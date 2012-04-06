#
# Background operations, such as received packet handling, are to be made here
#
__author__ = 'LucaFerrari MarcoBersani GiovanniLodi'

from threading import Thread
from threads.service_thread import ServiceThread
import socket

class BackgroundThread(Thread):

    def __init__(self, clientPeer, known_peers):
        super(BackgroundThread, self).__init__()
        self.clientPeer = clientPeer

    def run(self):
        #print "Background thread started"

        self.server_socket = None

        self.server_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.server_socket.bind(
            (self.clientPeer.ip, self.clientPeer.port)
        )

        self.server_socket.listen(10)
        while 1:
            #print "Waiting for connection "
            (socket_client, address) = self.server_socket.accept()
            s = ServiceThread(socket_client, self.clientPeer.ip, self.clientPeer.port)
            s.start()

