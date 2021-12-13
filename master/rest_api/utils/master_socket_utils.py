import zmq # For ZMQ
import time # For waiting a second for ZMQ connections
import math # For cutting the file in half
import random # For selecting a random half when requesting chunks



class MasterSocketUtils():

    def __init__(self):
        context = zmq.Context()
        # Socket to send chunk to Storage Nodes
        self.push_socket = context.socket(zmq.PUSH)
        self.push_socket.bind("tcp://*:5557")

        # Socket to receive chunk from Storage Nodes
        self.pull_socket = context.socket(zmq.PULL)
        self.pull_socket.bind("tcp://*:5558")

        # Publisher socket for broadcasts chunks requests 
        self.broadcast_socket = context.socket(zmq.PUB)
        self.broadcast_socket.bind("tcp://*:5559")

    
    def pushChunkToWorker(self, pb_file, file_chunk):
        self.push_socket.send_multipart([
            pb_file.SerializeToString(),
            file_chunk
        ])


    def recieveAck(self):
        return self.pull_socket.recv_string()




