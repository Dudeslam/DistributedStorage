import zmq # For ZMQ
import time # For waiting a second for ZMQ connections
import math # For cutting the file in half
import random

from zmq.backend import zmq_poll # For selecting a random half when requesting chunks


class SlaveSocketUtils:

    def __init__(self, server_address, node_name, pi_ips):
        
        # pull incomming chunk storage request
        pi1,pi2,pi3 = pi_ips
        self.pi1 = pi1
        self.pi2 = pi2
        self.pi3 = pi3

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


        self.slave_router = context.socket(zmq.ROUTER)
        self.slave_router.bind(f"tcp://*:600{node_name[-1]}")

        self.dealer_pi1 = context.socket(zmq.DEALER)
        self.dealer_pi2 = context.socket(zmq.DEALER)
        self.dealer_pi3 = context.socket(zmq.DEALER)
        
        self.dealer_pi1.setsockopt_string(zmq.IDENTITY, node_name)
        self.dealer_pi2.setsockopt_string(zmq.IDENTITY, node_name)
        self.dealer_pi3.setsockopt_string(zmq.IDENTITY, node_name)

        print(f"ips : {self.pi1}, {self.pi2}, {self.pi2}")
        self.dealer_pi1.connect(f"tcp://{self.pi1}:6001")
        self.dealer_pi2.connect(f"tcp://{self.pi2}:6002")
        self.dealer_pi3.connect(f"tcp://{self.pi3}:6003")

        # Use a Poller to monitor two sockets at the same time
        self.poller = zmq.Poller()
        self.poller.register(self.receiver, zmq.POLLIN)
        self.poller.register(self.subscriber, zmq.POLLIN)
        self.poller.register(self.dealer, zmq.POLLIN)

        self.poller.register(self.dealer_pi1, zmq.POLLIN)
        self.poller.register(self.dealer_pi2, zmq.POLLIN)
        self.poller.register(self.dealer_pi3, zmq.POLLIN)


    def awaitUpdateFromMaster(self):
        return dict(self.poller.poll())

    def isSlaveRequest(self, socket_dict):
        bool1 = self.dealer_pi1 in socket_dict
        bool2 = self.dealer_pi2 in socket_dict
        bool3 = self.dealer_pi3 in socket_dict
        return bool1 or bool2 or bool3

    def get_active_slave_dealer(self, socket_dict):
        if self.dealer_pi1 in socket_dict:
            return self.dealer_pi1
        elif self.dealer_pi2 in socket_dict:
            return self.dealer_pi2
        else:
            return self.dealer_pi3     



    def isBroadcastRequest(self, socket_dict):
        return self.subscriber in socket_dict

    def isStoreRequest(self, socket_dict):
        return self.receiver in socket_dict

    def isStoreRequestDealer(self, socket_dict):
        return self.dealer in socket_dict    

    def readBroadcastMessage(self):
        return self.subscriber.recv()

    def readSlaveRequest(self, active_socket):
        return active_socket.recv_multipart()

    def readStoreRequest(self):
        return self.receiver.recv_multipart()

    def readStoreRequestDealer(self):
        return self.dealer.recv_multipart()


    def sendChunkToMaster(self, filename, raw_bytes):
        self.sender.send_multipart([
                    bytes(filename, 'utf-8'),
                    raw_bytes
                ])
    
    def sendChunkToWorker(self, node, model, filechunk):
        self.slave_router.send_multipart([
            bytes(node, 'utf-8'),
            model.SerializeToString(),
            filechunk
        ])

    def acknowledgeToMaster(self, model):
        self.sender.send(model.SerializeToString())

    def sendResponse(self, filename):
        self.sender.send_string(filename) 
        
    
    
