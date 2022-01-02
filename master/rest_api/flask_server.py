import csv
import json
import logging
import sys

sys.path.insert(1, "../../")
from erasure_codes import reedsolomon
from models.file import File
from repositories import file_repository

sys.path.insert(1, "../../")
import models.messages_pb2 as pb_models
import metrics.metric_log as logger
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
import time


storageUtils = StorageUtils()
socketUtils = MasterSocketUtils()
log = ""
with open("../../config.txt") as f:
    masterip = f.readline().split('=')[1].strip()
    pi1 =  f.readline().split('=')[1].strip()
    pi2 =  f.readline().split('=')[1].strip()
    pi3 =  f.readline().split('=')[1].strip()
    log =  f.readline().split('=')[1].strip()
    
metric_log = logger.MetricLog(f"../../metrics/logs/{log}.csv")

app = Flask(__name__)

base_path = "exercise2"

file_handle = open(f'../../metrics/logs/erasure_server_results.csv', 'w')
csv_writer = csv.writer(file_handle)
fields = ['event', 'file_size', 'storage_mode', 'max_erasures', 'time']
csv_writer.writerow(fields)

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

def findDistinctBlock(part_filenames, ack_meta_data):
    for part_file in part_filenames:
        for node_meta_data in ack_meta_data:
            for filename_meta in node_meta_data[1]:
                if part_file == filename_meta:
                    return (part_file, node_meta_data[0])    


@app.route(f"/{base_path}/files/<int:k_replica>", methods=['POST'])
def add_files(k_replica):
    payload = request.get_json()
    filename = payload.get('filename')
    content_type = payload.get('content_type')
    file_data = b64decode(payload.get('contents_b64'))
    size = len(file_data)
    created = date.today()
    
    start_time = time.time()

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
            pb_file.type = "file"
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
            pb_file.type = "file"
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

    
    for block in range(len(k_replica_names)):
        _ = socketUtils.receiveAck()

        
    blocknammes_1 = [block[1] for block in k_replica_names if block[0] == 0]
    print(f"blocknammes_1 {blocknammes_1}")
    blocknammes_2 = [block[1] for block in k_replica_names if block[0] == 1]
    print(f"blocknammes_2 {blocknammes_2}")
    id = storageUtils.insert_file_meta_data(filename, size, content_type, created, blocknammes_1, blocknammes_2)
        
    endtime = time.time()

    replication_time = endtime - start_time
    metric_log.log_entry(str(replication_time) )


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

@app.route(f"/{base_path}/delegate/<int:k_replica>", methods=['POST'])
def delegate_work(k_replica):
    payload = request.get_json()
    filename = payload.get('filename')
    content_type = payload.get('content_type')
    file_data = b64decode(payload.get('contents_b64'))
    size = len(file_data)
    created = date.today()

    start_time = time.time()
    file_data_1 = file_data[:math.ceil(size/2.0)]
    file_data_2 = file_data[math.ceil(size/2.0):]
    # Generate two random chunk names for each half

    split = 2
    k_replica_names = []
    for i in range(split):
        for _ in range(k_replica):
            k_replica_names.append((i, id_generator(8)))   # (0, "ASASHDJASD")

           
    blocknammes_1 = [block[1] for block in k_replica_names if block[0] == 0]
    print(f"blocknammes_1 {blocknammes_1}")
    blocknammes_2 = [block[1] for block in k_replica_names if block[0] == 1]
    print(f"blocknammes_2 {blocknammes_2}")
    id = storageUtils.insert_file_meta_data(filename, size, content_type, created, blocknammes_1, blocknammes_2)

    node_list = get_node_list(socketUtils.number_of_connected_subs)
    print(f"node list : {node_list}")
    for block in range(2):
        if block == 0:
            pb_file = pb_models.delegate_file()
            pb_file.type = "delegate_file"
            pb_file.filenames.extend(blocknammes_1)

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
            pb_file = pb_models.delegate_file()
            pb_file.type = "delegate_file"
            pb_file.filenames.extend(blocknammes_2)

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
            socketUtils.pushChunkToWorkerRouter(random_node, pb_file, file_data_2)   
    
    for block in range(2):  
        print("Recheive ack to worker")
        _ = socketUtils.receiveAck()
    
    endtime = time.time()
    replication_time = endtime - start_time
    metric_log.log_entry(str(replication_time) )
    # Return the ID of the new file record with HTTP 201 (Created) status code
    return make_response({"id":id}, 201)


@app.route(f'/exercise3/files/<string:file_id>', methods=['GET'])
def download_file_erasure(file_id):
    file = file_repository.get_file(file_id)

    print(f"File requested: {file.fileName}")

    # Parse the storage details JSON string
    storage_details = json.loads(file.storage_details)

    print(f"File requested in storage mode: {file.storage_mode}")

    if file.storage_mode == 'erasure_coding_rs':
        start_time = time.time()

        coded_fragments = storage_details['coded_fragments']
        max_erasures = storage_details['max_erasures']

        tasks = reedsolomon.get_file_tasks(
            coded_fragments,
            max_erasures,
            file.size
        )

        for task in tasks:
            socketUtils.broadcastChunkRequest(task)
        
        end_time = time.time()
        total_time = end_time - start_time
        csv_writer.writerow(['erasure_get', file.size, file.storage_mode, max_erasures, total_time])

        # Receive all chunks and insert them into the symbols array
        symbols = []
        for _ in range(len(tasks)):
            result = socketUtils.pull_receive_multipart()
            # In this case we don't care about the received name, just use the
            # data from the second frame
            symbols.append({
                "chunkname": result[0].decode('utf-8'),
                "data": bytearray(result[1])
            })
        print("All coded fragments received successfully")

        # Reconstruct the original file data
        file_data = reedsolomon.decode_file(symbols)[:file.size]

        end_time = time.time()
        total_time = end_time - start_time
        csv_writer.writerow(['erasure_get_response', file.size, file.storage_mode, max_erasures, total_time])  

    elif file.storage_mode == 'erasure_coding_rs_random_worker':
        start_time = time.time()

        coded_fragments = storage_details['coded_fragments']
        max_erasures = storage_details['max_erasures']     

        task = pb_models.delegate_file()
        task.type = "WORKER_RETRIEVE_FILE_REQ"
        task.filenames.extend(coded_fragments)

        node_list = get_node_list(socketUtils.number_of_connected_subs)       
            
        random_node = None
        if (len(node_list) != 0):
            random.shuffle(node_list)
            random_node = node_list[0]
            node_list.remove(random_node)
        else:
            node_list = get_node_list(socketUtils.number_of_connected_subs)
            random.shuffle(node_list)
            random_node = node_list[0]
            node_list.remove(random_node)

        if random_node == 'node4':
            print("hey not node 4")
            random_node = 'node1'

        file_size_string = str(file.size)
        max_erasures_string = str(max_erasures)

        socketUtils.pushRequestToWorkerRouter(random_node, task, str.encode(file_size_string), str.encode(max_erasures_string))
        end_time = time.time()
        total_time = end_time - start_time
        csv_writer.writerow(['erasure_get_random_worker', file.size, file.storage_mode, max_erasures, total_time])

        print("Waiting to receive file from random worker")
        msg = socketUtils.pull_receive_multipart()

        print("Got file from random worker")
        end_time = time.time()
        total_time = end_time - start_time
        csv_writer.writerow(['erasure_get_random_worker_response', file.size, file.storage_mode, max_erasures, total_time])        

        # Reconstruct the original file data
        file_data = msg[0]

    else:
        raise NotImplementedError('Unsupported storage mode')

    return send_file(io.BytesIO(file_data), mimetype=file.content_type)


@app.route(f'/exercise3/files_mp', methods=['POST'])
def add_files_multipart():
    start_time = time.time()

    # Flask separates files from the other form fields
    payload = request.form
    files = request.files

    # Make sure there is a file in the request
    if not files or not files.get('file'):
        logging.error("No file was uploaded in the request!")
        return make_response("File missing!", 400)

    # Reference to the file under 'file' key
    file = files.get('file')
    # The sender encodes a the file name and type together with the file contents
    filename = file.filename
    content_type = file.mimetype
    # Load the file contents into a bytearray and measure its size
    data = bytearray(file.read())
    size = len(data)
    print("File received: %s, size: %d bytes, type: %s" % (filename, size, content_type))

    # Read the requested storage mode from the form (default value: 'raid1')
    storage_mode = payload.get('storage', 'erasure_coding_rs')
    print("Storage mode: %s" % storage_mode)

    if storage_mode == 'erasure_coding_rs':
        # Reed Solomon code
        # Parse max_erasures (everything is a string in request.form,
        # we need to convert to int manually), set default value to 1
        max_erasures = int(payload.get('max_erasures', 1))

        # Store the file contents with Reed Solomon erasure coding
        tasks, fragments = reedsolomon.get_store_file_tasks(data, max_erasures)
        fragment_names = list(map(lambda x: x.filename, tasks))

        print("Sending store data requests to other nodes")
        for task, fragment in zip(tasks, fragments):
            socketUtils.pushChunkToWorker(task, fragment)

        print("Awaiting responses from other nodes")
        for task_nbr in range(4):
            resp = socketUtils.receiveAck()
            print('Received: %s' % resp)

        end_time = time.time()
        total_time = end_time - start_time
        csv_writer.writerow(['erasure_write', size, storage_mode, max_erasures, total_time])

        storage_details = {
            "coded_fragments": fragment_names,
            "max_erasures": max_erasures
        }
    elif storage_mode == 'erasure_coding_rs_random_worker':
        # Make random worker encode and store file on nodes
        # Build task
        max_erasures = int(payload.get('max_erasures', 1))
        task = pb_models.delegate_erasure_file()
        task.max_erasures = max_erasures
        task.type = "WORKER_STORE_FILE_REQ"
        task.filename = filename

        node_list = get_node_list(socketUtils.number_of_connected_subs)

        random_node = None
        if (len(node_list) != 0):
            random.shuffle(node_list)
            random_node = node_list[0]
            node_list.remove(random_node)
        else:
            node_list = get_node_list(socketUtils.number_of_connected_subs)
            random.shuffle(node_list)
            random_node = node_list[0]
            node_list.remove(random_node)

        socketUtils.pushChunkToWorkerRouter('node1', task, data)

        end_time = time.time()
        total_time = end_time - start_time
        csv_writer.writerow(['erasure_write', size, storage_mode, max_erasures, total_time])

        # Await response from worker node
        msg = socketUtils.pull_receive_multipart()

        end_time = time.time()
        total_time = end_time - start_time
        csv_writer.writerow(['erasure_write_worker_response', size, storage_mode, max_erasures, total_time])

        task = pb_models.worker_store_file_response()
        task.ParseFromString(msg[0])

        storage_details = {
            "coded_fragments": list(task.fragments),
            "max_erasures": max_erasures
        }
    else:
        logging.error("Unexpected storage mode: %s" % storage_mode)
        return make_response("Wrong storage mode", 400)

    # Insert the File record in the DB

    file = File(fileName=filename,
                size=size, content_type=content_type,
                storage_mode=storage_mode,
                storage_details=json.dumps(storage_details))

    file_repository.add_file(file)
    file = file.to_dict()

    end_time = time.time()
    total_time = end_time - start_time
    csv_writer.writerow(['finished', size, storage_mode, max_erasures, total_time])
    return make_response({"id": file['id']}, 201)


@app.errorhandler(500)
def server_error(e):
    logging.exception("Internal error: %s", e)
    return make_response({"error": str(e)}, 500)

app.run(host="0.0.0.0", port=9000)
app.teardown_appcontext(storageUtils.close_db)
app.teardown_appcontext(file_handle.close())

