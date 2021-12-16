import sys
sys.path.insert(1, "../../")
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
import math # For cutting the file in half
import random # For selecting a random half when requesting chunks
import io # For sending binary data in a HTTP response
from base64 import b64decode



storageUtils = StorageUtils()
socketUtils = MasterSocketUtils()

app = Flask(__name__)

base_path = "exercise2"
#number_of_worker_nodes = 3

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

def get_random_node_list(number_of_nodes):
    node_list = []
    for i in range(socketUtils.number_of_connected_subs):
        randon_num = random.randint(1,number_of_nodes) 
        node_list.append(f"node{randon_num}")

    return node_list


def get_node_list(number_of_nodes):
    node_list = []
    for i in range(1, number_of_nodes+1):
        node_list.append(f"node{i}")
    return node_list


@app.route(f"/{base_path}/files/<int:k_replica>", methods=['POST'])
def add_files(k_replica):
    payload = request.get_json()
    filename = payload.get('filename')
    content_type = payload.get('content_type')
    file_data = b64decode(payload.get('contents_b64'))
    size = len(file_data)
    created = date.today()

    file_data_1 = file_data[:math.ceil(size/2.0)]
    file_data_2 = file_data[math.ceil(size/2.0):]
    # Generate two random chunk names for each half

    split = 2
    k_replica_names = []
    for i in range(split):
        for _ in range(k_replica):
            k_replica_names.append((i, id_generator(8)))   # (0, "ASASHDJASD")
   
    print(f"Genreated block names : {k_replica_names}")
    node_list = get_node_list(socketUtils.number_of_connected_subs)


    for block in k_replica_names:
        if block[0] == 0:
            pb_file = pb_models.file()
            pb_file.filename = block[1]
            random_node = None
            if(len(node_list) != 0):
                random.shuffle(node_list)
                random_node = node_list[0]
                node_list.remove(random_node)
            else:
                node_list = get_node_list(socketUtils.number_of_connected_subs)
                random.shuffle(node_list)
                random_node = node_list[0]
                node_list.remove(random_node)

            print(f"Sending part 1 to {random_node}")
            socketUtils.pushChunkToWorkerRouter(random_node, pb_file, file_data_1)
        else:
            pb_file = pb_models.file()
            pb_file.filename = block[1]

            random_node = None
            if(len(node_list) != 0):
                random.shuffle(node_list)
                random_node = node_list[0]
                node_list.remove(random_node)
            else:
                node_list = get_node_list(socketUtils.number_of_connected_subs)
                random.shuffle(node_list)
                random_node = node_list[0]
                node_list.remove(random_node)


            print(f"Sending part 2 to {random_node}")
            socketUtils.pushChunkToWorkerRouter(random_node,pb_file, file_data_2)    
        
        
    blocknammes_1 = [block[1] for block in k_replica_names if block[0] == 0]
    print(f"blocknammes_1 {blocknammes_1}")
    blocknammes_2 = [block[1] for block in k_replica_names if block[0] == 1]
    print(f"blocknammes_2 {blocknammes_2}")
    id = storageUtils.insert_file_meta_data(filename, size, content_type, created, blocknammes_1, blocknammes_2)

    # Return the ID of the new file record with HTTP 201 (Created) status code
    return make_response({"id":id}, 201)


def findDistinctBlock(part_filenames, ack_meta_data):
    for part_file in part_filenames:
        for node_meta_data in ack_meta_data:
            for filename_meta in node_meta_data[1]:
                if part_file == filename_meta:
                    return (part_file, node_meta_data[0])

    

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

    all_filenames = part1_filenames + part2_filenames
    # Broast cast chunk request to all workers (part1)
    all_files_model = pb_models.broadcast_request_file()
    all_files_model.filenames.extend(all_filenames)
    all_files_model.type = "broadcast_request_file"

    print(all_files_model.SerializeToString())   
    print(f"broadcasting files :  {all_files_model.filenames}")
    socketUtils.broadcastChunkRequest(all_files_model)

    ack_meta_data = []
    for _ in range(socketUtils.number_of_connected_subs):
        msg = socketUtils.receiveAcknowlegde()
        ack_model = pb_models.broadcast_response_node()
        ack_model.ParseFromString(msg)
        if(ack_model.hasFile):
            ack_meta_data.append((ack_model.node, ack_model.filenames))


    print(f"ach meta data {ack_meta_data}")

    broadcast_request_file = pb_models.broadcast_request_specefic()

    files1, node1 = findDistinctBlock(part1_filenames, ack_meta_data)
    files2, node2 = findDistinctBlock(part2_filenames, ack_meta_data)

    print(f"nodes = {node1} , {node2}")
    print(f"files = {files1} , {files2}")

    broadcast_request_file.nodes.extend([node1, node2])
    broadcast_request_file.filenames.extend([files1, files2])
    broadcast_request_file.type = "broadcast_request_specefic"

    socketUtils.broadcastSpecificRequest(broadcast_request_file)              
   
    file_data_parts = [None, None]
    for _ in range(len(broadcast_request_file.filenames)):
        result = socketUtils.receiveChunk()
        # First frame: file name (string)
        filename_received = result[0].decode('utf-8')
        print(f"File receivd {filename_received}")
        # Second frame: data
        chunk_data = result[1]
            # Setting frames in correct order
        if filename_received in part1_filenames:
            # The first part was received
            file_data_parts[0] = chunk_data
        elif filename_received in part2_filenames:
            # The second part was received
            file_data_parts[1] = chunk_data

    print("Both chunks received successfully")
    # Combine the parts and serve the file
    file_data = file_data_parts[0] + file_data_parts[1]
    return send_file(io.BytesIO(file_data), mimetype=file_as_dict['content_type'])


app.run(host="0.0.0.0", port=9000)
app.teardown_appcontext(storageUtils.close_db)

