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
        
    # Wait until we receive 3 responses from the workers
    for _ in range(number_of_worker_nodes):
        ack = socketUtils.recieveAck()
        print(f"Received: {ack}")

    id = storageUtils.insert_file_meta_data(filename, size, content_type, created, file_data_1_names, file_data_2_names)

    # Return the ID of the new file record with HTTP 201 (Created) status code
    return make_response({"id":id}, 201)



@app.route('/files/<int:file_id>', methods=['GET'])
def download_file(file_id):
    db = storageUtils.get_db()
    cursor = db.execute("SELECT * FROM `file` WHERE `id`=?", [file_id])
    if not cursor:
        return make_response({"message": "Error connecting to the database"}, 500)
    f = cursor.fetchone()
    # Convert to a Python dictionary
    f = dict(f)
    print("File requested: {}".format(f))
    # Return the binary file contents with the proper Content-Type header.
    return send_file(f"../storage/{f['blob_name']}", mimetype=f['content_type'])



app.run(host="localhost", port=9000)
app.teardown_appcontext(storageUtils.close_db)

