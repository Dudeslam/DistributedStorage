import sys
sys.path.insert(1,"../../")
import models.messages_pb2 as pb_models
from flask import Flask
from flask import Flask, make_response, request, send_file
from zmq.backend import Socket
from utils.storage_utils import StorageUtils
from utils.master_socket_utils import MasterSocketUtils
import base64
import random
import string
from datetime import date
import zmq # For ZMQ
import time # For waiting a second for ZMQ connections
import math # For cutting the file in half
import random # For selecting a random half when requesting chunks
import io # For sending binary data in a HTTP response
from base64 import b64decode




storageUtils = StorageUtils()
socketUtils = MasterSocketUtils()

app = Flask(__name__)

base_path = "exercise2"
number_of_worker_nodes = 3

@app.route(f"/{base_path}/helloworld")
def hello():
    return make_response({'message': 'Hello World!'})


def write_file(encoded_file):
    base64bytes = base64.b64decode(encoded_file)
    blop_id = id_generator()
    f = open(f"../storage/{blop_id}", "wb")
    f.write(base64bytes)
    f.close() 

    return blop_id

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


@app.route(f"/{base_path}/files", methods=['POST'])
def add_files():
    payload = request.get_json()
    filename = payload.get('filename')
    content_type = payload.get('content_type')
    file_data = b64decode(payload.get('contents_b64'))
    size = len(file_data)
    created = date.today()

    # RAID 1: cut the file in half and store both halves 2x
    file_data_1 = file_data[:math.ceil(size/2.0)]
    file_data_2 = file_data[math.ceil(size/2.0):]
    # Generate two random chunk names for each half
    file_data_1_names = [id_generator(8), id_generator(8)]
    file_data_2_names = [id_generator(8), id_generator(8)]
    print(f"Filenames for part 1: {file_data_1_names}")
    print(f"Filenames for part 2: {file_data_2_names}")

    #Send 2 'store data' Protobuf requests with the first half and chunk names
    for name in file_data_1_names:
        pb_file = pb_models.file()
        pb_file.filename = name
        socketUtils.pushChunkToWorker(pb_file, file_data_1)
    # Send 2 'store data' Protobuf requests with the second half and chunk names
    for name in file_data_2_names:
        pb_file = pb_models.file()
        pb_file.filename = name
        socketUtils.pushChunkToWorker(pb_file, file_data_2)

    id = storageUtils.insert_file_meta_data(filename, size, content_type, created, file_data_1_names, file_data_2_names)

    # Return the ID of the new file record with HTTP 201 (Created) status code
    return make_response({"id":id}, 201)



@app.route(f"/{base_path}/files/<int:file_id>",  methods=['GET'])
def download_file(file_id):
    fetched_metadata = storageUtils.get_metadata(file_id)
    if fetched_metadata == None: 
        return make_response({"message": "File not found"}, 404)
       
    # Convert to a Python dictionary
    file_as_dict = dict(fetched_metadata)
    # Select one chunk of each half
    part1_filenames = file_as_dict['part1_filenames'].split(',')
    part2_filenames = file_as_dict['part2_filenames'].split(',')
    part1_filename = part1_filenames[random.randint(0, len(part1_filenames)-1)]
    part2_filename = part2_filenames[random.randint(0, len(part2_filenames)-1)]
    
    # Broast cast chunk request to all workers (part1)
    model1 = pb_models.file()
    model1.filename = part1_filename
    print(f"broadcast request file : {model1.filename} ")
    socketUtils.broadcastChunkRequest(model1)

    # Broast cast chunk request to all workers (part2)
    model2 = pb_models.file()
    model2.filename = part2_filename
    print(f"broadcast request file : {model2.filename} ")
    socketUtils.broadcastChunkRequest(model2)

    # Receive both chunks and insert them to
    file_data_parts = [None, None]
    for _ in range(2):
        result = socketUtils.receiveChunk()
        # First frame: file name (string)
        filename_received = result[0].decode('utf-8')
        # Second frame: data
        chunk_data = result[1]
        print(f"Received {filename_received}")

        # Setting frames in correct order
        if filename_received == part1_filename:
            # The first part was received
            file_data_parts[0] = chunk_data
        else:
            # The second part was received
            file_data_parts[1] = chunk_data
    
    print("Both chunks received successfully")
    # Combine the parts and serve the file
    file_data = file_data_parts[0] + file_data_parts[1]

    return send_file(io.BytesIO(file_data), mimetype=file_as_dict['content_type'])


app.run(host="0.0.0.0", port=9000)
app.teardown_appcontext(storageUtils.close_db)

