__author__ = 'LucaFerrari MarcoBersani GiovanniLodi'

from threading import Thread
from managers.filesmanager import FilesManager
import socket

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

        self._socket.setblocking(1)

        try:
            self._socket.setblocking(1) # <-------- ??

            command = str(self._socket.recv(4))

            # Received package looking for a file
            if command == "QUER":
                pckt_id = str(self._socket.recv(16))
                peer_ip = str(self._socket.recv(15))
                peer_port = str(self._socket.recv(5))
                ttl = str(self._socket.recv(2))
                query = str(self._socket.recv(20))

                if int(ttl) > 1:
                    # decrease ttl propagate the message to the peers
                    ttl = str(int(ttl) - 1)
                    # TODO something like
                    known_peers = [] # <-- to be filled with objects
                    for peer in known_peers:
                        self._socket.send(command + pckt_id + peer_ip + peer_port + ttl + query)


                    # look for the requested file
                    for f in find_files(query):
                        md5 = calculate_md5_for_file_path(f)
                        filename = f.split('/')[-1:]
                        self._socket.send("AQUE" + pckt_id + ip + port + md5 + filename)

            # Received package in reply to a file research
            if command == "AQUE":
                print "AQUE received"
                pckt_id = str(self._socket.recv(16))
                peer_ip = str(self._socket.recv(15))
                peer_port = str(self._socket.recv(5))
                file_md5 = str(self._socket.recv(16))
                file_name = str(self._socket.recv(100))

                # Add the result to the result list and show it on screen

            # Received package looking for neighbour peers
            if command == "NEAR":
                print "NEAR received"
                pckt_id = str(self._socket.recv(16))
                peer_ip = str(self._socket.recv(15))
                peer_port = str(self._socket.recv(5))
                ttl = str(self._socket.recv(2))

                if int(ttl) > 1:
                    # decrease ttl and propagate the message to the peers
                    ttl = str(int(ttl) - 1)
                    # TODO something like
                    known_peers = [] # <-- to be filled with objects
                    for peer in known_peers:
                        self._socket.send(command + pckt_id + peer_ip + peer_port + ttl)


            # Received package in reply to a neighbour peer search
            if command == "ANEA":
                print "ANEA received "
                pckt_id = str(self._socket.recv(16))
                peer_ip = str(self._socket.recv(15))
                peer_port = str(self._socket.recv(5))

                # Add peer to known peers
                # TODO something like
                # known_peers.add(new Peer(peer_ip. peer_port)

            elif command == "":
                condition = False

            self._socket.close()
        except Exception, ex:
            condition = False
            print ex

        print "request processed correctly"
