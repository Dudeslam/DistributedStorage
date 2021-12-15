import sys
sys.path.insert(1,"../")
import os
import models.messages_pb2 as pb_models
from utils.slave_socket_utils import SlaveSocketUtils
import models.messages_pb2 as pb_models # Generated Protobuf messages

nodename = sys.argv[1]
data_folder = sys.argv[1] if len(sys.argv) > 1 else "./"
if data_folder != "./":
    try:
        os.mkdir('./'+data_folder)
    except FileExistsError as _:
        # OK, the folder exists
        pass

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

masterip = ""
with open("../config.txt") as f:
    masterip = f.readline().split('=')[1].strip()

print(f"connectiong to master ip : {masterip} ")
slave_socket_utils = SlaveSocketUtils(masterip)


while True:
    try:
    # Poll all sockets
        socks = slave_socket_utils.awaitUpdateFromMaster()
    except KeyboardInterrupt:
        break
    # At this point one or multiple sockets have received a message
    if slave_socket_utils.isStoreRequest(socks):
        print("StoreRequest rechieved")
       # Incoming message on the 'receiver' socket where we get tasks to store a chunk
        msg = slave_socket_utils.readStoreRequest()
        
        # Parse the Protobuf message from the first frame
        model = pb_models.file()
        model.ParseFromString(msg[0])
        # The data is the second frame
        data = msg[1]
        print(f"Chunk with name {model.filename} rechieved")
        # Store the chunk with the given filename
        chunk_local_path = data_folder+'/'+model.filename
        write_file(data, chunk_local_path)


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
                            break
                    except FileNotFoundError:
                    # The chunk is not stored by this node
                        pass

            print(model_broadcast.nodes)
            print(model_broadcast.filenames)


        else:
            pass
        # Parse the Protobuf message from the first frame
        #model_broadcast = pb_models.broadcast_request()
        #model_broadcast.ParseFromString(msg)
        #filenames = model_broadcast.filenames
        #print(f"chunk name request: {model_broadcast.filenames}")
#
        ## Try to load the requested file from the local file system,
        ## send response only if found
        #for filename in filenames:
        #    try:
        #        with open(data_folder+'/'+filename, "rb") as in_file:
        #            print(f"Found chunk {filename}, sending it back")
        #            slave_socket_utils.sendChunkToMaster(filename, in_file.read())
        #            break
        #    except FileNotFoundError:
        #    # The chunk is not stored by this node
        #        pass
#