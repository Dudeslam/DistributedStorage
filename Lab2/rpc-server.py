import gevent
import gevent.pywsgi
import gevent.queue
import base64

from tinyrpc.server.gevent import RPCServerGreenlets
from tinyrpc.dispatch import RPCDispatcher
from tinyrpc.protocols.jsonrpc import JSONRPCProtocol
from tinyrpc.transports.wsgi import WsgiServerTransport

dispatcher = RPCDispatcher()
transport = WsgiServerTransport(queue_class=gevent.queue.Queue)

# start wsgi server as a background-greenlet
wsgi_server = gevent.pywsgi.WSGIServer(('127.0.0.1', 5555), transport.handle)
gevent.spawn(wsgi_server.serve_forever)

rpc_server = RPCServerGreenlets(
    transport,
    JSONRPCProtocol(),
    dispatcher
)


@dispatcher.public
def reverse_string(s):
    return s[::-1]


@dispatcher.public
def save_file(fileName, b64_string):
    binary_data = base64.b64decode(b64_string)
    filename = write_file(binary_data, filename=fileName)
    return "File saved: {}".format(fileName)


def write_file(data, filename=None):
    if not filename:
        filename_length = 8
        filename = "".join([random.SystemRandom().choice(
            string.ascii_letters + string.digits) for n in range(filename_length)])

        filename += ".bin"

    try:
        with open("./" + filename, "wb") as f:
            f.write(data)
    except EnvironmentError as e:
        print("error writing file: {}".format(e))
        return None

    return filename


# in the main greenlet, run our rpc_server
rpc_server.serve_forever()
