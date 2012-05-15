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


    def login(self, tracker_ip, tracker_port = 80):
        try:
            login_sock = connect_socket(tracker_ip, tracker_port)
            login_sock.send("LOGI")
            login_sock.send(format_ip_address(get_local_ip(login_sock.getsockname()[0])))
            login_sock.send(format_port_number(self.local_port))


            response = read_from_socket(login_sock, 4) #read ALGI
            if response == "ALGI":
                my_session_id = read_from_socket(login_sock, 16)
                login_sock.close()

                UsersManager.set_my_session_id(my_session_id)
                klog("Done. My session id is: %s" % my_session_id)

                self.ui_handler.login_done(my_session_id)
            else:
                raise Exception("Response command error: %s" %response)
        except Exception, ex:
            klog(str(ex))
            self.ui_handler.login_done(None)

    def search_for_files(self, query):
        PacketsManager.add_new_generated_packet(p_id)

        my_superpeer = UsersManager.get_superpeer()

        try:
            sock = connect_socket(my_superpeer.ip, my_superpeer.port)
            sock.send("LOOK" + UsersManager.get_my_session_id() + format_query(query))
            klog("Started LOOK for file: %s" %query)

            if read_from_socket(sock, 4) == 'ALOO':
                files_count = int(read_from_socket(sock, 3))
                for i in range(0, files_count):
                    file_id = read_from_socket(sock, 16)
                    file_name = read_from_socket(sock, 100)
                    file_size = read_from_socket(sock, 10)
                    part_size = read_from_socket(sock, 6)
                    self.ui_handler.add_new_result_file(file_name, file_id, file_size, part_size)

            else:
                raise Exception("Response command error: %s. Wanted LOOK" % response)

        except Exception, ex:
            klog(str(ex))

    def logout(self):
        my_superpeer = UsersManager.get_superpeer()
        sock = connect_socket(my_superpeer.ip, 80)#my_superpeer.port)
        sock.send("LOGO" + UsersManager.get_my_session_id())
        response = read_from_socket(sock, 4)
        num_file_deleted = -1
        if response == "ALGO":
            num_file_deleted = int(read_from_socket(sock, 3))
            klog("LOGOUT Done. Deleted %d files" % num_file_deleted)
        else:
            klog("LOGOUT non eseguito")
        sock.close()
        return num_file_deleted

    def download_file(self, peer_ip, peer_port, md5, filename):
        downloadSocket = connect_socket(peer_ip, peer_port)
        downloadSocket.send("RETR")
        downloadSocket.send(decode_md5(md5))
        # Star a thread that will take care of the download and of the socket management
        dlThread = DownloadThread(downloadSocket, filename, md5, peer_ip, self.ui_handler)
        dlThread.start()

    def register_file_to_supernode(self, file):
        my_superpeer = UsersManager.get_superpeer()
        sock = connect_socket(my_superpeer.ip, 80)#my_superpeer.port)
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
        sock = connect_socket(my_superpeer.ip, 80)#my_superpeer.port)
        local_ip = get_local_ip(sock.getsockname()[0])
        sock.send("DEFF" + UsersManager.get_my_session_id())
        sock.send(decode_md5(file.hash))
        sock.close()

    def unregister_all_files_to_supernode(self):
        for file in FilesManager.shared_files():
            self.unregister_file(file)

