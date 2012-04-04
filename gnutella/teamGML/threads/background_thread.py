#
# Background operations, such as received packet handling, are to be made here
#
__author__ = 'LucaFerrari MarcoBersani GiovanniLodi'

from threading import Thread
import socket

class BackgroundThread(Thread):

    def __init__(self, ip, port):
        super(BackgroundThread, self).__init__()
        self.ip = ip
        self.port = port

    def run(self):
        #print "Background thread started"

        self.server_socket = None

        self.server_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.server_socket.bind(
            (self.ip, int(self.port))
        )

        self.server_socket.listen(10)
        while 1:
            #print "Waiting for connection "
            (socket_client, address) = self.server_socket.accept()
            s = ServiceThread(socket_client, self.ip, self.port)
            s.start()

