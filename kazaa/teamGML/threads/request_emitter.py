__author__ = 'LucaFerrari MarcoBersani GiovanniLodi'

import socket
from threading import Thread
from models.peer import Peer
import random
from managers.peersmanager import PeersManager
from managers.packetsmanager import PacketsManager
from managers.filesmanager import FilesManager
from managers.usersmanager import UsersManager
from custom_utils.formatting import *
from custom_utils.hashing import *
from custom_utils.logging import *
from custom_utils.sockets import *
from threads.download_thread import DownloadThread
from threads.service_thread import ServiceThread
import threading

TTL_FOR_SUPERPEERS_SEARCH = 4
TTL_FOR_FILES_SEARCH = 3

class RequestEmitter(object):

    def __init__(self, local_port):
        self.local_port = local_port
        self.ui_handler = None

    def search_for_superpeers(self, ttl = TTL_FOR_SUPERPEERS_SEARCH ):
        klog("Started query flooding for superpeers, ttl %s" %ttl)

        p_id = generate_packet_id(16)
        formatted_port = format_port_number(self.local_port)
        formatted_ttl = format_ttl(ttl)

        for peer in PeersManager.find_known_peers():
            sock = connect_socket(peer.ip, peer.port)
            local_ip = get_local_ip(sock.getsockname()[0])
            PacketsManager.add_new_generated_packet(p_id)
            sock.send("SUPE" + p_id + format_ip_address(local_ip) + formatted_port + formatted_ttl)
            sock.close()

        def _choose_random_superpeer():
            superpeers = PeersManager.find_known_peers(True)

            if len(superpeers) > 0:
                my_superpeer = superpeers[random.randrange(0, len(superpeers),1)]
                UsersManager.set_superpeer(my_superpeer)
                klog("Choose this superpeer: %s:%s" %(my_superpeer.ip, str(my_superpeer.port)))
                klog("Login...")

                login_sock = connect_socket(my_superpeer.ip, int(my_superpeer.port))
                login_sock.send("LOGI")
                login_sock.send(format_ip_address(get_local_ip(login_sock.getsockname()[0])))
                login_sock.send(format_port_number(self.local_port))

                try:
                    read_from_socket(login_sock, 4) #read ALGI
                    my_session_id = read_from_socket(login_sock, 16)
                    login_sock.close()

                    UsersManager.set_my_session_id(my_session_id)
                    klog("Done. My session id is: %s" %my_session_id)

                    self.ui_handler.superpeer_choosen(my_superpeer.ip, my_superpeer.port)
                    self.ui_handler.login_done(my_session_id)
                except Exception, ex:
                    klog(ex)

        threading.Timer(2, _choose_random_superpeer).start()

    def search_for_files(self, query, ttl = TTL_FOR_FILES_SEARCH ):
        p_id = generate_packet_id(16)
        PacketsManager.add_new_generated_packet(p_id)

        if UsersManager.is_super_node():
            # We need to search both locally and in the network
            PacketsManager.register_packet_id_as_local_search(p_id)

            # Perform a local search here.
            for file in FilesManager.find_files_by_query(query):
                owner = UsersManager.find_user_by_session_id(file.session_id)
                if owner:
                    self.ui_handler.add_new_result_file(file.filename, owner.ip, owner.port, encode_md5(file.hash))

            # ...and send a QUER in the network, its results will be handled properly and should not interfere with
            # the ones of the local search
            for superpeer in PeersManager.find_known_peers():
                sock = connect_socket(superpeer.ip, superpeer.port)
                local_ip = get_local_ip(sock.getsockname()[0])
                sock.send("QUER" + p_id + format_ip_address(local_ip) + format_port_number(self.local_port) + format_ttl(ttl) + format_query(query))
                sock.close()
            klog("Started query flooding for files: %s ttl: %s" %(query,ttl) )
        else:
            my_superpeer = UsersManager.get_superpeer()
            if my_superpeer:
                sock = connect_socket(my_superpeer.ip, my_superpeer.port)
                sock.send("FIND" + UsersManager.get_my_session_id() + format_query(query))
                klog("Started query flooding for files: %s ttl: %s" %(query,ttl) )
                # We need also some handling for those stupid peers that do not close the socket...
                #time.sleep(5)
                if read_from_socket(sock, 4) == 'AFIN':
                    ServiceThread.afin_received(sock, self.ui_handler)

    def download_file(self, peer_ip, peer_port, md5, filename):
        downloadSocket = connect_socket(peer_ip, peer_port)
        downloadSocket.send("RETR")
        downloadSocket.send(decode_md5(md5))
        # Star a thread that will take care of the download and of the socket management
        dlThread = DownloadThread(downloadSocket, filename, md5, peer_ip, self.ui_handler)
        dlThread.start()

    def register_file_to_supernode(self, file):
        my_superpeer = UsersManager.get_superpeer()
        sock = connect_socket(my_superpeer.ip, my_superpeer.port)
        local_ip = get_local_ip(sock.getsockname()[0])
        sock.send("ADFF" + UsersManager.get_my_session_id())
        sock.send(decode_md5(file.hash))
        sock.send(format_filename(file.filename))
        sock.close()

    def register_all_files_to_supernode(self):
        for file in FilesManager.shared_files():
            self.register_file_to_supernode(file)

    def unregister_file(self, file):
        my_superpeer = UsersManager.get_superpeer()
        sock = connect_socket(my_superpeer.ip, my_superpeer.port)
        local_ip = get_local_ip(sock.getsockname()[0])
        sock.send("DEFF" + UsersManager.get_my_session_id())
        sock.send(decode_md5(file.hash))
        sock.close()

    def unregister_all_files_to_supernode(self):
        for file in FilesManager.shared_files():
            self.unregister_file(file)

