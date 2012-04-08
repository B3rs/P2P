__author__ = 'LucaFerrari MarcoBersani GiovanniLodi'

from threading import Thread
from managers.filesmanager import FilesManager
from managers.peersmanager import PeersManager
from custom_utils.formatting import *
import socket

class ServiceThread(Thread):

    def __init__(self, socket, ip, port, ui_handler):
        self._socket = socket

        self.ip = format_ip_address(ip)
        self.port = format_port_number(port)

        self.ui_handler = ui_handler

        super(ServiceThread, self).__init__()


    def run(self):

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

                    for peer in PeersManager.find_known_peers():
                        self._socket.send(command + pckt_id + peer_ip + peer_port + ttl + query)


                    # look for the requested file
                    for f in FilesManager.find_files_by_query(query):
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
                self.ui_handler.add_new_result_file(file_name, peer_ip, peer_port. file_md5)


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
                    for peer in PeersManager.find_known_peers():
                        self._socket.send(command + pckt_id + peer_ip + peer_port + ttl)


            # Received package in reply to a neighbour peer search
            if command == "ANEA":
                print "ANEA received "
                pckt_id = str(self._socket.recv(16))
                peer_ip = str(self._socket.recv(15))
                peer_port = str(self._socket.recv(5))

                # Add peer to known peers
                PeersManager.add_new_peer(peer_ip, peer_port)
                self.ui_handler.peers_changed()


            elif command == "":
                condition = False

            self._socket.close()
        except Exception, ex:
            condition = False
            print ex

        print "request processed correctly"
