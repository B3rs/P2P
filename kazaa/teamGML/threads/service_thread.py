__author__ = 'LucaFerrari MarcoBersani GiovanniLodi'

from threading import Thread
import time
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

    aquers = {}

    def __init__(self, socket, ip, port, ui_handler):
        self._socket = socket

        self.ip = format_ip_address(ip)
        self.port = format_port_number(port)

        self.ui_handler = ui_handler

        super(ServiceThread, self).__init__()


    def add_file(self, session_id, hash, file_name):
        user = UsersManager.find_user_by_session_id(session_id)
        if user:
            FilesManager.create_file(file_name, hash, user)

    def remove_file(self, session_id, hash):
        file = FilesManager.find_file_by_hash_and_sessionid(hash, session_id)
        if file:
            FilesManager.delete_file(file)

    def login_user(self, ip, port):
        user = UsersManager.create_user(ip, port)
        return user.session_id

    def logout_user(self, session_id):
        user = UsersManager.find_user_by_session_id(session_id)
        if user:
            numdeleted = FilesManager.delete_files_for_user(user)
            UsersManager.delete_user(user)
            return numdeleted
        else:
            return -1

    @classmethod
    def initialize_for_pckt(cls, search_id):
        ServiceThread.aquers[search_id] = []

    @classmethod
    def add_query_result(cls, search_id, ip, port, hash, filename):
        if ServiceThread.aquers.has_key(search_id):
            ServiceThread.aquers[search_id].push({'search_id': search_id, 'ip':ip, 'port': port, 'hash':hash, 'filename':filename})
        else:
            print "AQUE refused for timeout"

    @classmethod
    def get_query_results(cls, search_id):
        if ServiceThread.aquers.has_key(search_id):
            return ServiceThread.aquers[search_id]

    @classmethod
    def clear_pending_query(cls, search_id):
        del ServiceThread.aquers[search_id]

    @classmethod
    def afin_received(cls, sock, ui_handler):
        num = int(read_from_socket(sock, 3))
        klog("%d files found" %num)

        for i in range(0, num):
            file_md5 = str(read_from_socket(sock, 16))
            file_name = str(read_from_socket(sock, 100)).strip(" ")
            copies_num = int(read_from_socket(sock, 3))

            for j in range(0, copies_num):
                peer_ip = str(sock.recv(15))
                peer_port = str(sock.recv(5))

                # Add the result to the result list and show it on screen if is nor my filw
                if peer_ip != format_ip_address(get_local_ip(sock.getsockname()[0])):
                    klog("Found %s from %s:%s" % (file_name,peer_ip, peer_port))
                    ui_handler.add_new_result_file(file_name, peer_ip, peer_port, encode_md5(file_md5))


    def run(self):

        try:
            self._socket.setblocking(1) # <-------- ??

            command = str(self._socket.recv(4))

            #
            # FILES
            #

            # Received package looking for a file
            if command == "QUER":

                if UsersManager.is_super_node():
                    pckt_id = str(self._socket.recv(16))
                    sender_ip = str(self._socket.recv(15))
                    sender_port = str(self._socket.recv(5))
                    ttl = int(self._socket.recv(2))
                    query = str(self._socket.recv(20))

                    klog("%s pid: %s %s:%s ttl: %s query: %s" % (command, pckt_id, sender_ip, sender_port, ttl, query))

                    if not PacketsManager.is_packet_id_known(pckt_id):

                        PacketsManager.add_new_packet(pckt_id, sender_ip)

                        if int(ttl) > 0:

                            # look for the requested file
                            for f in FilesManager.find_files_by_query(query):
                                command = "AQUE"
                                sock = connect_socket(sender_ip, sender_port)

                                sock.send(command + pckt_id + format_ip_address(self.ip) + format_port_number(self.port))
                                sock.send(decode_md5(f.hash))
                                sock.send(format_filename(f.filename))
                                klog("command sent %s pkid:%s %s:%s md5: %s filename: %s" % (command, pckt_id, self.ip, self.port, f.hash, f.filename))

                                sock.close()

                            # decrease ttl propagate the message to the peers
                            ttl = format_ttl(ttl -1)

                            if int(ttl) > 0:
                                for superpeer in PeersManager.find_known_peers(superpeers=True):
                                    #query flooding to the known superpeers peers except for the sender
                                    if not PeersManager.are_same_peer(superpeer, Peer(sender_ip, sender_port)):
                                        sock = connect_socket(superpeer.ip, superpeer.port)
                                        sock.send(command + pckt_id + sender_ip + sender_port + str(ttl) + query)
                                        klog("command sent to %s:%s: %s pkid:%s %s:%s ttl: %s query: %s" % (superpeer.ip, superpeer.port, command, pckt_id, sender_ip, sender_port, ttl, query))
                                        sock.close()



            # Received package in reply to a file research
            elif command == "AQUE":
                klog("AQUE received")
                search_id = str(self._socket.recv(16))
                sender_ip = str(self._socket.recv(15))
                sender_port = str(self._socket.recv(5))
                hash = encode_md5(self._socket.recv(16))
                filename = str(self._socket.recv(100)).strip(" ")
                if PacketsManager.is_local_search(search_id):
                    if PacketsManager.is_generated_packet_still_valid(search_id):
                        klog("Found %s from %s:%s" % (filename, sender_ip, sender_port))
                        self.ui_handler.add_new_result_file(filename, sender_ip, sender_port, hash)
                else:
                    ServiceThread.add_query_result(search_id, sender_ip, sender_port, hash, filename)

            elif command == "FIND":
                if UsersManager.is_super_node():
                    session_id = str(self._socket.recv(16))
                    query = str(self._socket.recv(20))
                    p_id = generate_packet_id(16)

                    # Launch a request to the other super peers with the query
                    for superpeer in PeersManager.find_known_peers(True):
                        sock = connect_socket(superpeer.ip, superpeer.port)
                        local_ip = get_local_ip(sock.getsockname()[0])
                        sock.send("QUER" + p_id + format_ip_address(local_ip) + format_port_number(self.local_port) + format_ttl(ttl) + format_query(query))
                        sock.close()

                    ServiceThread.initialize_for_pckt(p_id)    #enable the receive of packets for this query

                    time.sleep(20)

                    #search_id is the packet id of QUER request, it identifies univocally the query
                    superpeers_result = ServiceThread.get_query_results(p_id)
                    my_directory_result = FilesManager.find_files_by_query(query)
                    ServiceThread.clear_pending_query(p_id)
                    result = {}
                    #costruisco l array di risultati
                    for r in superpeers_result:
                        if result.has_key(r.hash):
                            result[r.hash].peers.append([{'ip':r.ip, 'port':r.port}])
                        else:
                            result[r.hash] = {'filemd5':r.hash, 'filename':r.filename, 'peers':[{'ip':r.ip, 'port':r.port}]}

                    for f in my_directory_result:
                        if f.is_my_file():
                            if result.has_key(f.hash):
                                result[f.hash]['peers'].append({'ip':self.ip, 'port':self.port})
                            else:
                                result[f.hash] = {'filemd5':f.hash, 'filename':f.filename, 'peers':[{'ip':self.ip, 'port':self.port}]}
                        else:
                            u = UsersManager.find_user_by_session_id(f.session_id)
                            if result.has_key(f.hash):
                                result[f.hash]['peers'].append({'ip':u.ip, 'port':u.port})
                            else:
                                result[f.hash] = {'filemd5':f.hash, 'filename':f.filename, 'peers':[{'ip':u.ip, 'port':u.port}]}
                        #must send AFIN

                    #self._socket.close()


                    peer = UsersManager.find_user_by_session_id(session_id)
                    #sock = connect_socket(peer.ip, peer.port)
                    sock = self._socket
                    sock.send("AFIN"+format_deletenum(len(result)))
                    for key, r in result.items():
                        sock.send(decode_md5(r['filemd5']))
                        sock.send(format_filename(r['filename']))
                        sock.send(format_deletenum(len(r['peers'])))
                        for peer in r['peers']:
                            sock.send(format_ip_address(peer['ip']))
                            sock.send(format_port_number(peer['port']))
                    #threading.Timer(20, self.search_finished, args=(p_id,)).start()  #calls the fun function with p_id as argument
                    klog("Sent AFIN")

            elif command == "AFIN":
                klog("AFIN received")
                ServiceThread.afin_received(self._socket, self.ui_handler)



            #
            # PEERS
            #

            elif command == "LOGI":
                if UsersManager.is_super_node():
                    peer_ip = str(read_from_socket(self._socket, 15))
                    peer_port = str(read_from_socket(self._socket, 5))

                    if UsersManager.find_user_by_ip(peer_ip) is not None:
                        self._socket.send("ALGI"+"0"*16)
                        klog("Sent ALGI" + "0"*16 + "to: %s" %(peer_ip))
                    else:
                        session_id = self.login_user(peer_ip, peer_port)
                        klog("Received a LOGI, from: %s, port: %s. Session id created: %s" %(peer_ip, peer_port, session_id))
                        self._socket.send("ALGI" + session_id)
                        klog("Sent ALGI to: %s, port: %s" %(peer_ip, peer_port))
                        self.ui_handler.add_new_peer(peer_ip, peer_port)

            elif command == "ALGI":
                #Normally this is done in the RequestEmitter, but we have the same code here to
                #prevent crashes in case of closed and re-opened socket
                session_id = str(read_from_socket(self._socket, 16))
                klog("ALGI received form super peer: %s", session_id)
                UsersManager.set_my_session_id(session_id)
                self.ui_handler.login_done(session_id)

            elif command == "LOGO":
                peer_session_id = str(read_from_socket(self._socket, 16))
                peer = UsersManager.find_user_by_session_id(peer_session_id)
                peer_ip = peer.ip
                peer_port = peer.port
                klog("Received a LOGO, from session_id: %s. Peer: %s:%s" %(peer_session_id, peer_ip, peer_port))

                delete_num = self.logout_user(peer_session_id)
                self._socket.send("ALGO"+ format_deletenum(delete_num))
                klog("Sent ALGO to session_id: %s deletenum: %d" %(peer_session_id, delete_num))
                self.ui_handler.remove_peer(peer_ip, peer_port)

            elif command == "ALGO":
                delete_num = read_from_socket(self._socket, 3)
                klog("ALGO received. delete num: %s" %delete_num)

                UsersManager.set_my_session_id("")
                klog("TODO: destroy the listening client???")

            # Received package looking for super-peer
            elif command == "SUPE":
                klog("SUPE received")
                pckt_id = str(read_from_socket(self._socket, 16))
                sender_ip = str(read_from_socket(self._socket, 15))
                sender_port = str(read_from_socket(self._socket, 5))
                ttl = int(read_from_socket(self._socket, 2))

                if not PacketsManager.is_packet_id_known(pckt_id):

                    PacketsManager.add_new_packet(pckt_id, sender_ip)

                    if int(ttl) > 0:

                        if UsersManager.is_super_node():
                            # Respond with an ASUP
                            sock = connect_socket(sender_ip, sender_port)
                            sock.send("ASUP" + pckt_id + self.ip + self.port + str(ttl))
                            klog("command sent to %s:%s: ASUP pkid:%s %s:%s ttl: %s" % (sender_ip, sender_port, pckt_id, self.ip, self.port, ttl))
                            sock.close()

                        # decrease ttl and propagate the message to the peers/superpeers
                        ttl = format_ttl(ttl -1)

                        if int(ttl) > 0:
                            # propagate the SUPE
                            for peer in PeersManager.find_known_peers():
                                if not PeersManager.are_same_peer(peer, Peer(sender_ip, sender_port)):
                                    sock = connect_socket(peer.ip, peer.port)
                                    sock.send("SUPE" + pckt_id + sender_ip + sender_port + str(ttl))
                                    klog("command sent to %s:%s: SUPE pkid:%s %s:%s ttl: %s" % (peer.ip, peer.port, pckt_id, sender_ip, sender_port, ttl))
                                    sock.close()


            # Received package in reply to a super-peer search
            elif command == "ASUP":

                pckt_id = str(self._socket.recv(16))
                peer_ip = str(self._socket.recv(15))
                peer_port = str(self._socket.recv(5))

                klog("ASUP received from %s:%s" %(peer_ip, peer_port))

                if PacketsManager.is_generated_packet_still_valid(pckt_id):
                    #Check if the superpeer war already added as a normal peer
                    if PeersManager.is_known_peer(Peer(peer_ip, peer_port)):
                        PeersManager.become_superpeer(peer_ip, peer_port)
                    else:
                        PeersManager.add_new_peer(Peer(peer_ip, peer_port, True))

                    self.ui_handler.add_new_superpeer(peer_ip, peer_port)

            # Received package asking for a file
            elif command == "RETR":
                klog("RETR received")
                CHUNK_DIM = 128

                md5 = encode_md5(self._socket.recv(16))

                self._socket.send("ARET")   #sending the ack command
                remote_ip = self._socket.getpeername()[0]
                my_session_id = UsersManager.get_my_session_id()

                # Get the file matching the md5
                klog("finding file with md5: %s, session_id %s" %(md5, my_session_id))

                file = FilesManager.find_file_by_hash(md5)

                if file:
                    klog("i have found the file: %s stored in %s" % (file.filename, file.filepath))

                    # Chunks
                    size = file_size(file.filepath)
                    bytes_sent = 0
                    chunks_num = int(size // CHUNK_DIM)
                    leftover = size % CHUNK_DIM
                    if leftover != 0.0:
                        chunks_num += 1

                    self._socket.send(format_chunks_number(chunks_num)) #sending the chunks number

                    #open the file
                    file2send= open(file.filepath, 'rb')
                    chunk = file2send.read(CHUNK_DIM)

                    while chunk != '':
                        self._socket.send(format_chunk_length(len(chunk)))  #sending the chunk length
                        bytes_sent += self._socket.send(chunk)    #sending the chunk

                        percent = bytes_sent*100/size
                        self.ui_handler.upload_file_changed(file.filename, file.hash, remote_ip, percent)

                        chunk = file2send.read(CHUNK_DIM)
                    file2send.close()

                    klog("upload completed: %s" %file.filename)
                    self.ui_handler.upload_file_changed(file.filename, file.hash, remote_ip, 100)

                else:
                    klog("I do not have this file!")

            elif command == "ADFF":
                peer_session_id = str(read_from_socket(self._socket, 16))
                file_hash = encode_md5(read_from_socket(self._socket, 16))
                file_name = str(read_from_socket(self._socket, 100)).strip(' ')
                klog("Received a ADFF, from: %s. Hash: %s. Filename: %s." %(peer_session_id, file_hash, file_name))
                self.add_file(peer_session_id, file_hash, file_name)

            elif command == "DEFF":
                peer_session_id = str(read_from_socket(self._socket, 16))
                file_hash = encode_md5(read_from_socket(self._socket, 16))
                self.remove_file(peer_session_id, file_hash)
                klog("Received a DELF, from: %s. Hash: %s." %(peer_session_id, file_hash))

            if command == "":
                condition = False

            # Close the socket
            self._socket.close()

        except Exception, ex:
            condition = False
            print ex

