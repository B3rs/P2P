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
        login_sock = connect_socket(tracker_ip, tracker_port)
        login_sock.send("LOGI")
        login_sock.send(format_ip_address(get_local_ip(login_sock.getsockname()[0])))
        login_sock.send(format_port_number(self.local_port))

        try:
            response = read_from_socket(login_sock, 4) #read ALGI
            if response == "ALGI":
                my_session_id = read_from_socket(login_sock, 16)
                login_sock.close()

                UsersManager.set_my_session_id(my_session_id)
                klog("Done. My session id is: %s" % my_session_id)

                UsersManager.set_tracker(Peer(tracker_ip,tracker_port))
                klog("Done. My session id is: %s" % my_session_id)

                self.ui_handler.login_done(my_session_id)
            else:
                raise Exception("Response command error: %s" %response)
        except Exception, ex:
            klog(ex)

    def search_for_files(self, query):
        PacketsManager.add_new_generated_packet(p_id)

        my_tracker = UsersManager.get_tracker()

        try:
            sock = connect_socket(my_tracker.ip, my_tracker.port)
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
            klog(ex)

    def logout(self):
        my_tracker = UsersManager.get_tracker()
        sock = connect_socket(my_tracker.ip, 80)
        sock.send("LOGO" + UsersManager.get_my_session_id())
        response = read_from_socket(sock, 4)
        num_file_deleted = -1
        if response == "ALOG":
            num_file_deleted = int(read_from_socket(sock, 10))
            klog("LOGOUT Done. Deleted %d files" % num_file_deleted)
        elif response == "NLOG":
            num_files = int(read_from_socket(sock, 10))
            klog("LOGOUT refused from directory, you are the source for %s files" % num_files)
        sock.close()
        return num_file_deleted

    def download_file(self):
        pass
        #TODO: dobbiamo implementare che cerchi periodicamente le parti e che vada poi a scaricarle tramite la download_part. Fare nuovo thread?

    def download_part(self, peer_ip, peer_port, file_id, file_part, filename):
        downloadSocket = connect_socket(peer_ip, peer_port)
        downloadSocket.send("RETP")
        downloadSocket.send(file_id)
        downloadSocket.send(file_part)
        # Star a thread that will take care of the download and of the socket management
        dlThread = DownloadThread(downloadSocket, filename, file_id, file_part, peer_ip, self.ui_handler)
        dlThread.start()

    def register_part_to_tracker(self, file, part_num):
        my_tracker = UsersManager.get_tracker()
        sock = connect_socket(my_tracker.ip, my_tracker.port)
        local_ip = get_local_ip(sock.getsockname()[0])
        sock.send("RPAD" + UsersManager.get_my_session_id())
        sock.send(file.id)
        sock.send(format_partnum(part_num))

        #TODO: leggiti APAD
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

