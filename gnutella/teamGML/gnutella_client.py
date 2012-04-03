__author__ = 'LucaFerrari MarcoBersani GiovanniLodi'

from managers.filesmanager import FilesManager
import socket, os, sys
from threading import Thread
from custom_utils.logging import klog
from custom_utils.hashing import decode_md5, encode_md5, calculate_md5_for_file_path


class ServiceThread(Thread):
    def __init__(self, socket, ip, port):
        self._socket = socket
        self.ip = ip
        self.port = port
        super(ServiceThread, self).__init__()

    # TODO
    def find_files(self, query_string):
        if query_string != "":
            return FilesManager.find_files_by_query(query_string)
        else:
            return []

    def run(self):
        print "thread started"
        self._socket.setblocking(1)

        try:

            self._socket.setblocking(1) # <--------

            command = str(self._socket.recv(4))

            if command == "QUER":
                pckt_id = str(self._socket.recv(16))
                peer_ip = str(self._socket.recv(15))
                peer_port = str(self._socket.recv(5))
                ttl = str(self._socket.recv(2))
                query = str(self._socket.recv(20))

                if ttl > 1:
                    for f in find_files(query):
                        md5 = calculate_md5_for_file_path(f)
                        filename = f.split('/')[-1:]
                        self._socket.send("AQUE" + pckt_id + ip + port + md5 + filename)

            elif command == "":
                condition = False

            self._socket.close()
        except Exception, ex:
            condition = False
            print ex

        print "request processed correctly"

class ClientThread(Thread):
    #questo thread deve essere lanciato all'inizio e non deve mai uscire

    def __init__(self):
        super(ServiceThread, self).__init__()

    #definisco i vari metodi

    def run(self):

        print "started the client thread"

        while 1:
            print "che cosa desideri fare?"
            print "1)cercare un file"
            print "2)aggiornare la lista dei peer"
            cmdn = sys.stdin.read()

            if cmdn == 1:
                pass
            elif cmdn == 2:
                pass
            else:
                print "comando non valido"



class GnutellaPeer(object):

    def __init__(self):

        self.server_socket = None
        print "Init Gnutella peer"
        self.server_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Error checking
        if len(sys.argv) < 3:
            print "Usage $ python gnutella ip port"
            sys.exit()

        self.ip = sys.argv[1]
        self.port = sys.argv[2]
        
        self.server_socket.bind(
            (self.ip, int(self.port))
        )

    def start(self):
        print "Gnutella started on %s:%s" %(self.ip, self.port)

        self.server_socket.listen(10)
        while 1:
            print "Waiting for connection "
            (socket_client, address) = self.server_socket.accept()
            s = ServiceThread(socket_client, self.ip, self.port)
            s.start()


if __name__ == "__main__":
    ns = GnutellaPeer()
    ns.start()