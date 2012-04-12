__author__ = 'LucaFerrari MarcoBersani GiovanniLodi'

from threading import Thread
from managers.filesmanager import FilesManager
from managers.peersmanager import PeersManager
from custom_utils.formatting import *
from custom_utils.hashing import *
from custom_utils.sockets import *
from custom_utils.logging import klog
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
                sender_ip = str(self._socket.recv(15))
                sender_port = str(self._socket.recv(5))
                ttl = int(self._socket.recv(2))
                query = str(self._socket.recv(20))

                klog("%s pid: %s %s:%s ttl: %s query: %s" % (command, pckt_id, sender_ip, sender_port, ttl, query))

                if int(ttl) > 1:
                    # decrease ttl propagate the message to the peers
                    ttl = format_ttl(ttl -1)

                    for peer in PeersManager.find_known_peers():
                        sock = connect_socket(peer.ip, peer.port)
                        sock.send(command + pckt_id + sender_ip + sender_port + ttl + query)
                        klog("command sent to %s:%s: %s pkid:%s %s:%s ttl: %s query: %s" % (peer.ip, peer.port, command, pckt_id, sender_ip, sender_port, ttl, query))
                        sock.close()


                    # look for the requested file
                    for f in FilesManager.find_files_by_query(query):
                        md5 = calculate_md5_for_file_path(f)
                        filename = f.split('/')[-1]
                        command = "AQUE"
                        sock = connect_socket(sender_ip, sender_port)
                        sock.send(command + pckt_id + sender_ip + sender_port + md5 + filename)
                        klog("command sent %s pkid:%s %s:%s md5: %s filename: %s" % (command, pckt_id, sender_ip, sender_port, md5, filename))

                        sock.close()

            # Received package in reply to a file research
            if command == "AQUE":
                print "AQUE received"
                pckt_id = str(self._socket.recv(16))
                peer_ip = str(self._socket.recv(15))
                peer_port = str(self._socket.recv(5))
                file_md5 = str(self._socket.recv(16))
                file_name = str(self._socket.recv(100)).strip(" ")

                # Add the result to the result list and show it on screen
                self.ui_handler.add_new_result_file(file_name, peer_ip, peer_port, file_md5)


            # Received package looking for neighbour peers
            if command == "NEAR":
                print "NEAR received"
                pckt_id = str(self._socket.recv(16))
                sender_ip = str(self._socket.recv(15))
                sender_port = str(self._socket.recv(5))
                ttl = int(self._socket.recv(2))

                if ttl > 1:
                    # decrease ttl and propagate the message to the peers
                    ttl = format_ttl(ttl -1)

                    for peer in PeersManager.find_known_peers():
                        sock = connect_socket(peer.ip, peer.port)
                        sock.send(command + pckt_id + sender_ip + sender_port + ttl)
                        klog("command sent to %s:%s: %s pkid:%s %s:%s ttl: %s" % (peer.ip, peer.port, command, pckt_id, sender_ip, sender_port, ttl))

                        sock.close()

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
