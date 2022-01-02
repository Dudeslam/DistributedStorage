import string
import sys
import json
sys.path.insert(1, "../")
from erasure_codes import reedsolomon
from repositories import file_repository
import os
from utils.slave_socket_utils import SlaveSocketUtils
import models.messages_pb2 as pb_models # Generated Protobuf messages
import random

MAX_CHUNKS_PER_FILE = 10
number_of_nodes = 4
nodename = sys.argv[1]
print(nodename)
data_folder = sys.argv[1] if len(sys.argv) > 1 else "./"
if data_folder != "./":
    try:
        os.mkdir('./'+data_folder)
    except FileExistsError as _:
        # OK, the folder exists
        pass

#region helper methods

def get_node_list(number_of_nodes):
    node_list = []
    for i in range(1, number_of_nodes+1):
        node_list.append(f"node{i}")
    return node_list

def random_string(length=8):
    """
    Returns a random alphanumeric string of the given length.
    Only lowercase ascii letters and numbers are used.

    :param length: Length of the requested random string
    :return: The random generated string
    """
    return ''.join([random.SystemRandom().choice(string.ascii_letters + string.digits) for n in range(length)])
#

def write_file(data, filename=None):
    """
    Write the given data to a local file with the given filename

    :param data: A bytes object that stores the file contents
    :param filename: The file name. If not given, a random string is generated
    :return: The file name of the newly written file, or None if there was an error
    """
    if not filename:
        # Generate random filename
        filename = random_string(length=8)
        # Add '.bin' extension
        filename += ".bin"
    
    try:
        # Open filename for writing binary content ('wb')
        # note: when a file is opened using the 'with' statment, 
        # it is closed automatically when the scope ends
        with open('./'+filename, 'wb') as f:
            f.write(data)
    except EnvironmentError as e:
        print("Error writing file: {}".format(e))
        return None
    
    return filename
#endregion

masterip = ""
pi1 = ""
pi2 = ""
pi3 = ""
with open("../config.txt") as f:
    masterip = f.readline().split('=')[1].strip()
    pi1 =  f.readline().split('=')[1].strip()
    pi2 =  f.readline().split('=')[1].strip()
    pi3 =  f.readline().split('=')[1].strip()

print(f"connectiong to master ip : {masterip} ")
slave_socket_utils = SlaveSocketUtils(masterip, nodename, (pi1,pi2, pi3))


while True:
    try:
    # Poll all sockets
        socks = slave_socket_utils.awaitUpdateFromMaster()
    except KeyboardInterrupt:
        break
    # At this point one or multiple sockets have received a message
    if slave_socket_utils.isStoreRequestDealer(socks):
        print("StoreRequest rechieved")
       # Incoming message on the 'receiver' socket where we get tasks to store a chunk
        ## OLD
        #msg = slave_socket_utils.readStoreRequest()
        msg = slave_socket_utils.readStoreRequestDealer()
        # Parse the Protobuf message from the first frame
        temp_model = pb_models.file()
        temp_model.ParseFromString(msg[0])

        if temp_model.type == "file":
            model = pb_models.file()
            model.ParseFromString(msg[0])

            data = msg[1]
            print(f"Chunk with name {model.filename} rechieved")
            # Store the chunk with the given filename
            chunk_local_path = data_folder+'/'+model.filename
            write_file(data, chunk_local_path)
            slave_socket_utils.sendResponse(model.filename)


        elif temp_model.type == "delegate_file":
            model = pb_models.delegate_file()
            model.ParseFromString(msg[0])
            data = msg[1]

            number_of_request_replica = len(model.filenames)
            # Store the chunk with first filename
            chunk_local_path = data_folder+'/'+model.filenames[len(model.filenames)-1]
            write_file(data, chunk_local_path)

            node_list = get_node_list(number_of_nodes)
            node_list.remove(nodename)

            for block in range(number_of_request_replica-1):
                random_node = None
                if(len(node_list) != 0):
                    random.shuffle(node_list)
                    random_node = node_list[0]
                    node_list.remove(random_node)
                else:
                    node_list = get_node_list(number_of_nodes)
                    node_list.remove(nodename)
                    random.shuffle(node_list)
                    random_node = node_list[0]
                    node_list.remove(random_node)
            
                pb_model =  pb_models.file()
                pb_model.filename = model.filenames[block]
                pb_model.type = "file"

                print(f"Sending block: {pb_model.filename} to {random_node}")
                slave_socket_utils.sendChunkToWorker(random_node,pb_model, data)

            for _ in range(number_of_request_replica-1):
                print("Rechevied ack from worker")
                _ = slave_socket_utils.recheiveAck()

            slave_socket_utils.sendResponse("")
        elif temp_model.type == "STORE_FRAGMENT_DATA_REQ":
            # Parse the Protobuf message from the first frame
            task = pb_models.file()
            task.ParseFromString(msg[0])

            # The data starts with the second frame, iterate and store all frames
            for i in range(0, len(msg) - 1):
                data = msg[1 + i]

                print('Chunk to save: %s, size: %d bytes' %
                      (task.filename + "." + str(i), len(data)))

                # Store the chunk with the given filename
                chunk_local_path = data_folder + '/' + task.filename + "." + str(i)
                write_file(data, chunk_local_path)
                print("Chunk saved to %s" % chunk_local_path)

            # Send response (just the file name)
            slave_socket_utils.sendResponse(task.filename)

        elif temp_model.type == "WORKER_STORE_FILE_REQ":
            print("Starting to store file on the storage nodes")
            task = pb_models.delegate_erasure_file()
            task.ParseFromString(msg[0])
            data = msg[1]

            # Store the file contents with Reed Solomon erasure coding
            tasks, fragments = reedsolomon.get_store_file_tasks(bytearray(data), task.max_erasures)

            fragment_names = list(map(lambda x: x.filename, tasks))
            # Store a fragment on current node
            task = tasks.pop()
            fragment = fragments.pop()
            write_file(fragment, f'{data_folder}/{task.filename}')
            print(f"Stored {task.filename} on this node")

            print("Sending store data requests to other nodes")
            node_list = get_node_list(number_of_nodes)
            node_list.remove(nodename)

            for task, fragment in zip(tasks, fragments):
                random_node = None
                if (len(node_list) != 0):
                    random.shuffle(node_list)
                    random_node = node_list[0]
                    node_list.remove(random_node)
                else:
                    node_list = get_node_list(number_of_nodes)
                    node_list.remove(nodename)
                    random.shuffle(node_list)
                    random_node = node_list[0]
                    node_list.remove(random_node)

                pb_model = pb_models.file()
                pb_model.filename = task.filename
                pb_model.type = "file"

                print(f"Sending block: {pb_model.filename} to {random_node}")
                slave_socket_utils.sendChunkToWorker(random_node, pb_model, fragment)

            for _ in range(4-1):
                print("Rechevied ack from worker")
                _ = slave_socket_utils.recheiveAck()

            print("File stored on nodes")

            print("Sending response to lead node")
            task = pb_models.worker_store_file_response()
            print(fragment_names)
            task.fragments[:] = fragment_names
            slave_socket_utils.sender_send_multipart([task.SerializeToString()])

        elif temp_model.type == "WORKER_RETRIEVE_FILE_REQ":
            task = pb_models.delegate_file()
            task.ParseFromString(msg[0])

            encoded_file_size = msg[1]
            encoded_max_erasures = msg[2]


            coded_fragments = task.filenames
            file_size = int(encoded_file_size.decode())
            max_erasures = int(encoded_max_erasures.decode())


            print("Starting to retreive file on random storage node")            

            tasks = reedsolomon.get_file_tasks(
                coded_fragments,
                max_erasures,
                file_size
            )

            print("Distributing tasks")

            node_list = get_node_list(number_of_nodes)
            node_list.remove(nodename)

            symbols = []
            count = 0

            for task in tasks:
                print(task.filename)
                print(task.type)
                pb_model = pb_models.broadcast_request_fragment()
                pb_model.filename = task.filename
                pb_model.type = task.type  
                

                for node in node_list: 
                    slave_socket_utils.getFragmentFromWorker(node, pb_model)

                for i in range(1):
                    try:
                        with open(data_folder +'/'+ task.filename, "rb") as in_file:
                            print("Found chunk %s, on master" % task.filename)
                            symbols.append({
                                "chunkname": task.filename,
                                "data": bytearray(in_file.read())
                            })
                            count = 1


                    except FileNotFoundError:
                        # This is OK here
                        break

            print("Waiting for fragments")

            for _ in range(len(tasks) - count):
                result = slave_socket_utils.recheiveFragmentFromRandomNodes()
                # In this case we don't care about the received name, just use the
                # data from the second frame
                print("Got chunk named: " + result[1].decode('utf-8'))
                symbols.append({
                    "chunkname": result[1].decode('utf-8'),
                    "data": bytearray(result[2])
                })
            print("All coded fragments received successfully")

            print("Reconstructing the original file data")
            # Reconstruct the original file data
            file_data = reedsolomon.decode_file(symbols)[:file_size]

            print("Sending file to master")
            slave_socket_utils.sendFileToMaster(file_data)



    if slave_socket_utils.isStoreRequest(socks):
        print("StoreRequest rechieved")
        # Incoming message on the 'receiver' socket where we get tasks to store a chunk
        ## OLD
        # msg = slave_socket_utils.readStoreRequest()
        msg = slave_socket_utils.readStoreRequest()
        # Parse the Protobuf message from the first frame
        temp_model = pb_models.file()
        temp_model.ParseFromString(msg[0])

        if temp_model.type == "STORE_FRAGMENT_DATA_REQ":
            # Parse the Protobuf message from the first frame
            task = pb_models.file()
            task.ParseFromString(msg[0])

            # The data starts with the second frame, iterate and store all frames
            for i in range(0, len(msg) - 1):
                data = msg[1 + i]

                print('Chunk to save: %s, size: %d bytes' %
                      (task.filename + "." + str(i), len(data)))

                # Store the chunk with the given filename
                chunk_local_path = data_folder + '/' + task.filename + "." + str(i)
                write_file(data, chunk_local_path)
                print("Chunk saved to %s" % chunk_local_path)

            # Send response (just the file name)
            slave_socket_utils.sendResponse(task.filename)

        elif temp_model.type == "WORKER_STORE_FILE_REQ":
            print("Starting to store file on the storage nodes")
            task = pb_models.worker_store_file_request()
            task.ParseFromString(msg[0])
            data = msg[1]

            # Store the file contents with Reed Solomon erasure coding
            tasks, fragments = reedsolomon.get_store_file_tasks(bytearray(data), task.max_erasures)

            fragment_names = list(map(lambda x: x.filename, tasks))
            # Store a fragment on current node
            task = tasks.pop()
            fragment = fragments.pop()
            write_file(fragment, f'{data_folder}/{task.filename}')
            print(f"Stored {task.filename} on this node")

            print("Sending store data requests to other nodes")
            node_list = get_node_list(number_of_nodes)
            node_list.remove(nodename)

            for task, fragment in zip(tasks, fragments):
                random_node = None
                if (len(node_list) != 0):
                    random.shuffle(node_list)
                    random_node = node_list[0]
                    node_list.remove(random_node)
                else:
                    node_list = get_node_list(number_of_nodes)
                    node_list.remove(nodename)
                    random.shuffle(node_list)
                    random_node = node_list[0]
                    node_list.remove(random_node)

                pb_model = pb_models.file()
                pb_model.filename = task.filename
                pb_model.type = "file"

                print(f"Sending block: {pb_model.filename} to {random_node}")
                slave_socket_utils.sendChunkToWorker(random_node, pb_model, fragment)

            for _ in range(4 - 1):
                print("Rechevied ack from worker")
                _ = slave_socket_utils.recheiveAck()

            print("File stored on nodes")

            print("Sending response to lead node")
            task = pb_models.worker_store_file_response()
            print(fragment_names)
            task.fragments[:] = fragment_names
            slave_socket_utils.sender_send_multipart([task.SerializeToString()])

            raise NotImplementedError
  
    if slave_socket_utils.isSlaveRequest(socks):
        active_dealer_sock = slave_socket_utils.get_active_slave_dealer(socks)

        msg = slave_socket_utils.readSlaveRequest(active_dealer_sock)
        model = pb_models.file()
        model.ParseFromString(msg[0])

        if(model.type == "FRAGMENT_DATA_REQ"):
            task = pb_models.broadcast_request_fragment()
            task.ParseFromString(msg[0])

            print("Data chunk request from random node: %s" % task.filename)

            # Try to load all fragments with this name
            # First frame is the filename
            #frames = [bytes(task.filename, 'utf-8')]
            # Subsequent frames will contain the chunks' data
            for i in range(1):
                try:
                    with open(data_folder +'/'+ task.filename, "rb") as in_file:
                        print("Found chunk %s, sending it back" % task.filename)
                        slave_socket_utils.sendFragmentToMaster(active_dealer_sock, task.filename, in_file.read())
                        # Add chunk as a new frame
                        #frames.append(in_file.read())

                except FileNotFoundError:
                    # This is OK here
                    break
           

        else:
            data = msg[1]
            print(f"Chunk with name {model.filename} rechieved")
            # Store the chunk with the given filename
            chunk_local_path = data_folder+'/'+model.filename
            write_file(data, chunk_local_path)
            slave_socket_utils.sendAck(active_dealer_sock)

    if slave_socket_utils.isBroadcastRequest(socks):
        print("Broadcast rechieved")
        # Incoming message on the 'subscriber' socket where we get retrieve requests
        msg = slave_socket_utils.readBroadcastMessage()
        model_broadcast = pb_models.broadcast_request_file()
        model_broadcast.ParseFromString(msg)
        print(f"type = {model_broadcast.type}" )
        # broadcast_request_file, broadcast_response_node, broadcast_request_specefic
        if(model_broadcast.type == "broadcast_request_file"):
            # Parse the Protobuf message from the first frame
            print("is broadcast_request_file")
            model_broadcast = pb_models.broadcast_request_file()
            model_broadcast.ParseFromString(msg)
            filenames = model_broadcast.filenames

            broadcast_response_node = pb_models.broadcast_response_node()
            broadcast_response_node.node = nodename
            broadcast_response_node.hasFile = False
            filesnames_list = []
            for i, filename in enumerate(filenames):
                try:
                    with open(data_folder+'/'+filename, "rb") as in_file:
                        print(f"Found chunk {filename} adding to response model")
                        filesnames_list.append(filename)
                        broadcast_response_node.hasFile = True
                except FileNotFoundError:
                # The chunk is not stored by this node
                    pass
            broadcast_response_node.filenames.extend(filesnames_list)
            print("Sending acknowledgeToMaster")
            slave_socket_utils.acknowledgeToMaster(broadcast_response_node)
                    
        elif (model_broadcast.type == "broadcast_request_specefic"):
            print("Specific request rechieved")
            model_broadcast = pb_models.broadcast_request_specefic()
            model_broadcast.ParseFromString(msg)

            if nodename in model_broadcast.nodes:
                for filename in model_broadcast.filenames:
                    try:
                        with open(data_folder+'/'+filename, "rb") as in_file:
                            print(f"Found chunk {filename}, sending it back")
                            slave_socket_utils.sendChunkToMaster(filename, in_file.read())
                    except FileNotFoundError:
                    # The chunk is not stored by this node
                        pass

            print(model_broadcast.nodes)
            print(model_broadcast.filenames)

        elif (model_broadcast.type == "FRAGMENT_DATA_REQ"):
            task = pb_models.broadcast_request_fragment()
            task.ParseFromString(msg)

            print("Data chunk request: %s" % task.filename)

            # Try to load all fragments with this name
            # First frame is the filename
            frames = [bytes(task.filename, 'utf-8')]
            # Subsequent frames will contain the chunks' data
            for i in range(0, MAX_CHUNKS_PER_FILE):
                try:
                    with open(data_folder + '/' + task.filename + "." + str(i), "rb") as in_file:
                        print("Found chunk %s, sending it back" % task.filename)
                        # Add chunk as a new frame
                        frames.append(in_file.read())

                except FileNotFoundError:
                    # This is OK here
                    break

            # Only send a result if at least one chunk was found
            if (len(frames) > 1):
                slave_socket_utils.sender_send_multipart(frames)
        else:
            pass
