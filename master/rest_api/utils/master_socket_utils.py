import zmq # For ZMQ
import time # For waiting a second for ZMQ connections
import math # For cutting the file in half
import random # For selecting a random half when requesting chunks
from zmq.utils.monitor import recv_monitor_message
import threading


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
        self.number_of_connected_subs = 0
        self.broadcast_socket = context.socket(zmq.PUB)
        self.broadcast_socket.bind("tcp://*:5559")
        self.monitor = self.broadcast_socket.get_monitor_socket()

        self.EVENT_MAP = self.init_event_map()
        t = threading.Thread(target=self.event_monitor, args=(self.monitor,))
        t.start()
    

        self.router = context.socket(zmq.ROUTER)
        self.router.bind("tcp://*:6000")

    def event_monitor(self, monitor):
        while monitor.poll():
            evt = recv_monitor_message(monitor)
            evt.update({'description': self.EVENT_MAP[evt['event']]})
            print("Event: {}".format(evt))
            if evt["description"] == "EVENT_ACCEPTED":
                self.number_of_connected_subs +=1
            if evt["description"] == "EVENT_DISCONNECTED": 
                self.number_of_connected_subs -=1
            if evt['event'] == zmq.EVENT_MONITOR_STOPPED:
                break
            print(f"number of connections {self.number_of_connected_subs}")
            
        monitor.close()
        print()
        print("event monitor thread done!")

    def init_event_map(self):
        EVENT_MAP = {}
        print("Event names:")
        for name in dir(zmq):
            if name.startswith('EVENT_'):
                value = getattr(zmq, name)
                print("%21s : %4i" % (name, value))
                EVENT_MAP[value] = name
        return EVENT_MAP        
        
    def pushChunkToWorker(self, pb_file, file_chunk):
        self.push_socket.send_multipart([
            pb_file.SerializeToString(),
            file_chunk
        ])

    def pushChunkToWorkerRouter(self, worker_id, pb_file, file_chunk):
        self.router.send_multipart([
            bytes(worker_id, 'utf-8'),
            pb_file.SerializeToString(),
            file_chunk
        ])    

    def broadcastChunkRequest(self, model):
        self.broadcast_socket.send(model.SerializeToString())
    
    def broadcastSpecificRequest(self, model):
        self.broadcast_socket.send(model.SerializeToString())

    def receiveAck(self):
        return self.pull_socket.recv_string()

    def receive(self):
        return self.pull_socket.recv_string()


    def receiveChunk(self):
        return self.pull_socket.recv_multipart()

    def receiveAcknowlegde(self):
        return self.pull_socket.recv()

    def broadcast_send_multipart(self, multipart):
        self.broadcast_socket.send_multipart(multipart)

    def pull_receive_multipart(self):
        return self.pull_socket.recv_multipart()


