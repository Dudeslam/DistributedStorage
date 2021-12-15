import zmq # For ZMQ
import time # For waiting a second for ZMQ connections
import math # For cutting the file in half
import random # For selecting a random half when requesting chunks


class SlaveSocketUtils:

    def __init__(self, server_address, node_name):
        
        # pull incomming chunk storage request

        context = zmq.Context()
        self.receiver = context.socket(zmq.PULL)
        self.receiver.connect(f"tcp://{server_address}:5557")

        # Push chunk storage result
        self.sender = context.socket(zmq.PUSH)
        self.sender.connect(f"tcp://{server_address}:5558")

        # Subcribe to master - send chunk if worker has it
        self.subscriber = context.socket(zmq.SUB)
        self.subscriber.connect(f"tcp://{server_address}:5559")
        # Receive every message (empty subscription)
        self.subscriber.setsockopt(zmq.SUBSCRIBE, b'')


        self.dealer = context.socket(zmq.DEALER)
        self.dealer.setsockopt_string(zmq.IDENTITY, node_name)
        self.dealer.connect(f"tcp://{server_address}:6000")

        # Use a Poller to monitor two sockets at the same time
        self.poller = zmq.Poller()
        self.poller.register(self.receiver, zmq.POLLIN)
        self.poller.register(self.subscriber, zmq.POLLIN)
        self.poller.register(self.dealer, zmq.POLLIN)


    def awaitUpdateFromMaster(self):
        return dict(self.poller.poll())

    def isBroadcastRequest(self, socket_dict):
        return self.subscriber in socket_dict

    def isStoreRequest(self, socket_dict):
        return self.receiver in socket_dict

    def isStoreRequestDealer(self, socket_dict):
        return self.dealer in socket_dict    

    def readBroadcastMessage(self):
        return self.subscriber.recv()

    def readStoreRequest(self):
        return self.receiver.recv_multipart()

    def readStoreRequestDealer(self):
        return self.dealer.recv_multipart()


    def sendChunkToMaster(self, filename, raw_bytes):
        self.sender.send_multipart([
                    bytes(filename, 'utf-8'),
                    raw_bytes
                ])
    
    def acknowledgeToMaster(self, model):
        self.sender.send(model.SerializeToString())

    def sendResponse(self, filename):
        self.sender.send_string(filename) 
        
    
    
