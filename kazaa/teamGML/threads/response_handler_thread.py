#
# Background operations, such as received packet handling, are to be made here
#
__author__ = 'LucaFerrari MarcoBersani GiovanniLodi'

from threading import Thread
from service_thread import ServiceThread
from custom_utils import sockets
import socket

class ResponseHandlerThread(Thread):

    def __init__(self, port, ui_handler):
        super(ResponseHandlerThread, self).__init__()
        self.port = port
        self.ui_handler = ui_handler

    def run(self):
        #print "Background thread started"

        self.server_socket = None

        self.server_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.ip = self.server_socket.getsockname()[0]

        self.server_socket.bind(
            (self.ip, self.port)
        )

        self.server_socket.listen(10)
        while 1:
            #print "Waiting for connection "
            (socket_client, address) = self.server_socket.accept()
            # This (should) return the correct local ip, it needs a host to evaluate it
            my_remote_ip = sockets.get_local_ip(socket_client.getsockname()[0])
            s = ServiceThread(socket_client, my_remote_ip, self.port, self.ui_handler)
            s.start()

