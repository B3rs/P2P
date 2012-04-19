__author__ = 'LucaFerrari MarcoBersani GiovanniLodi'

from threading import Thread
from managers.filesmanager import FilesManager
from managers.peersmanager import PeersManager
from managers.packetsmanager import PacketsManager
from managers.usersmanager import UsersManager
from models.peer import Peer
from models.file import File
from custom_utils.formatting import *
from custom_utils.hashing import *
from custom_utils.sockets import *
from custom_utils.files import file_size
from custom_utils.logging import klog
import os

class ServiceThread(Thread):

    def __init__(self, socket, is_superpeer, ip, port, ui_handler):
        self._socket = socket

        self.is_superpeer = is_superpeer

        self.ip = format_ip_address(ip)
        self.port = format_port_number(port)

        self.ui_handler = ui_handler

        super(ServiceThread, self).__init__()

    #
    # TODO unstub!
    #
    def login_user(self, ip, port):
        return "1234567890ABCDEF"
    def logout_user(self, session_id):
        return 1



    def run(self):

        try:
            self._socket.setblocking(1) # <-------- ??

            command = str(self._socket.recv(4))

            #
            # FILES
            #

            # Received package looking for a file
            if command == "QUER":
                pckt_id = str(self._socket.recv(16))
                sender_ip = str(self._socket.recv(15))
                sender_port = str(self._socket.recv(5))
                ttl = int(self._socket.recv(2))
                query = str(self._socket.recv(20))

                klog("%s pid: %s %s:%s ttl: %s query: %s" % (command, pckt_id, sender_ip, sender_port, ttl, query))

                if not PacketsManager.is_packet_id_known(pckt_id):

                    PacketsManager.add_new_packet(pckt_id, sender_ip)

                    if int(ttl) > 1:
                        # decrease ttl propagate the message to the peers
                        ttl = format_ttl(ttl -1)

                        for peer in PeersManager.find_known_peers():
                            #query flooding to the known peers except for the sender
                            if not PeersManager.are_same_peer(peer, Peer(sender_ip, sender_port)):
                                sock = connect_socket(peer.ip, peer.port)
                                sock.send(command + pckt_id + sender_ip + sender_port + str(ttl) + query)
                                klog("command sent to %s:%s: %s pkid:%s %s:%s ttl: %s query: %s" % (peer.ip, peer.port, command, pckt_id, sender_ip, sender_port, ttl, query))
                                sock.close()


                        # look for the requested file
                        for f in FilesManager.find_files_by_query(query):
                            md5 = f.md5
                            filename = f.filename
                            command = "AQUE"
                            sock = connect_socket(sender_ip, sender_port)
                            sent = 0
                            sent += sock.send(command + pckt_id + format_ip_address(self.ip) + format_port_number(self.port))
                            sent += sock.send(decode_md5(md5))
                            sent += sock.send(format_filename(filename))
                            klog("command sent %s pkid:%s %s:%s md5: %s filename: %s" % (command, pckt_id, self.ip, self.port, md5, filename))

                            sock.close()

            # Received package in reply to a file research
            if command == "AQUE":
                klog("AQUE received")
                pckt_id = str(self._socket.recv(16))
                peer_ip = str(self._socket.recv(15))
                peer_port = str(self._socket.recv(5))
                file_md5 = str(self._socket.recv(16))
                file_name = str(self._socket.recv(100)).strip(" ")

                if PacketsManager.is_generated_packet_still_valid(pckt_id):
                    # Add the result to the result list and show it on screen
                    self.ui_handler.add_new_result_file(file_name, peer_ip, peer_port, encode_md5(file_md5))


            #
            # PEERS
            #

            if command == "LOGI":
                if self.is_superpeer:
                    peer_ip = str(self._socket.recv(15))
                    peer_port = str(self._socket.recv(5))

                    if UsersManager.find_user_by_ip(peer_ip) is not None:
                        self._socket.send("ALGI"+"0"*16)
                        klog("Sent ALGI" + "0"*16 + "to: %s" %(peer_ip))
                    else:
                        session_id = str(self.login_user(peer_ip, peer_port))
                        klog("Received a LOGI, from: %s, port: %s. Session id created: %s" %(peer_ip, peer_port, session_id))
                        self._socket.send("ALGI" + session_id)
                        klog("Sent ALGI to: %s, port: %s" %(peer_ip, peer_port))

            if command == "ALGI":
                session_id = str(self._socket.recv(16))
                # TODO store the session_id somewhere !
                klog("ALGI received form super peer")
                pass

            if command == "LOGO":
                peer_session_id = str(self._socket.recv(16))
                delete_num = self.logout_user(peer_session_id)
                klog("Received a LOGO, from session_id: %s" %(peer_session_id))
                self._socket.send("ALGO"+"{0:03d}".format(delete_num))
                klog("Sent ALGO to session_id: %s" %(peer_session_id))

            if command == "ALGO":
                print "ALGO received, it's such a sad thing :("

            # Received package looking for super-peer
            if command == "SUPE":
                klog("SUPE received")
                pckt_id = str(self._socket.recv(16))
                sender_ip = str(self._socket.recv(15))
                sender_port = str(self._socket.recv(5))
                ttl = int(self._socket.recv(2))

                if not PacketsManager.is_packet_id_known(pckt_id):

                    PacketsManager.add_new_packet(pckt_id, sender_ip)

                    if ttl > 1:
                        # decrease ttl and propagate the message to the peers/superpeers
                        ttl = format_ttl(ttl -1)

                        if self.is_superpeer:
                            # Respond with an ASUP
                            sock = connect_socket(sender_ip, sender_port)
                            sock.send("ASUP" + pckt_id + self.ip + self.port + ttl)
                            klog("command sent to %s:%s: ASUP pkid:%s %s:%s ttl: %s" % (sender_ip, sender_port, pckt_id, self.ip, self.port, ttl))
                            sock.close()

                        # propagate the SUPE
                        for peer in PeersManager.find_known_peers():
                            if not PeersManager.are_same_peer(peer, Peer(sender_ip, sender_port)):
                                sock = connect_socket(peer.ip, peer.port)
                                sock.send("SUPE" + pckt_id + sender_ip + sender_port + ttl)
                                klog("command sent to %s:%s: SUPE pkid:%s %s:%s ttl: %s" % (peer.ip, peer.port, pckt_id, sender_ip, sender_port, ttl))
                                sock.close()


                    # show yourself to the peer
                    sock = connect_socket(sender_ip, sender_port)
                    sock.send("ASUP" + pckt_id + self.ip + self.port)
                    sock.close()

            # Received package in reply to a super-peer search
            if command == "ASUP":

                pckt_id = str(self._socket.recv(16))
                peer_ip = str(self._socket.recv(15))
                peer_port = str(self._socket.recv(5))

                klog("ASUP received from %s:%s" %(peer_ip, peer_port))

                if PacketsManager.is_generated_packet_still_valid(pckt_id):
                    # Add peer to known peers
                    PeersManager.add_new_peer(peer_ip, peer_port)
                    self.ui_handler.peers_changed()

            # Received package asking for a file
            if command == "RETR":
                klog("RETR received")
                CHUNK_DIM = 128

                md5 = encode_md5(self._socket.recv(16))

                self._socket.send("ARET")   #sending the ack command
                remote_ip = self._socket.getpeername()[0]

                # Get the file matching the md5

                file = FilesManager.find_file_by_md5(md5)
                if file:
                    klog("i have found the file: %s" % file.filename)

                    # Chunks
                    size = file_size(os.path.join(file.filepath, file.filename))
                    bytes_sent = 0
                    chunks_num = int(size // CHUNK_DIM)
                    leftover = size % CHUNK_DIM
                    if leftover != 0.0:
                        chunks_num += 1

                    self._socket.send(format_chunks_number(chunks_num)) #sending the chunks number

                    #open the file
                    file2send= open(os.path.join(file.filepath, file.filename), 'rb')
                    chunk = file2send.read(CHUNK_DIM)

                    while chunk != '':
                        self._socket.send(format_chunk_length(len(chunk)))  #sending the chunk length
                        bytes_sent += self._socket.send(chunk)    #sending the chunk

                        percent = bytes_sent*100/size
                        self.ui_handler.upload_file_changed(file.filename, file.md5, remote_ip, percent)

                        chunk = file2send.read(CHUNK_DIM)
                    file2send.close()

                    klog("upload completed: %s" %file.filename)
                    self.ui_handler.upload_file_changed(file.filename, file.md5, remote_ip, 100)

                else:
                    klog("file by md5 not found")

            if command == "":
                condition = False

            # Close the socket
            self._socket.close()

        except Exception, ex:
            condition = False
            print ex

        klog("request processed correctly")