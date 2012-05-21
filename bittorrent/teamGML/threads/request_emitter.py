__author__ = 'LucaFerrari MarcoBersani GiovanniLodi'

import socket
from threading import Timer
from models.peer import Peer
import random, binascii

from managers.filesmanager import FilesManager
from managers.usersmanager import UsersManager
from custom_utils.formatting import *
from custom_utils.hashing import *
from custom_utils.logging import *
from custom_utils.sockets import *
from threads.download_queue_thread import DownloadQueueThread
from threads.download_thread import DownloadThread
from threads.service_thread import ServiceThread
import math

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

                UsersManager.set_tracker(Peer(tracker_ip,tracker_port))

                self.ui_handler.login_done(my_session_id)
            else:
                raise Exception("Response command error: %s" %response)
        except Exception, ex:
            klog(str(ex))
            self.ui_handler.login_done(None)

    def search_for_files(self, query):
        my_tracker = UsersManager.get_tracker()

        try:
            sock = connect_socket(my_tracker.ip, my_tracker.port)
            sock.send("LOOK" + UsersManager.get_my_session_id() + format_query(query))
            klog("Started LOOK for file: %s" %query)

            if read_from_socket(sock, 4) == 'ALOO':
                files_count = int(read_from_socket(sock, 3))
                for i in range(0, files_count):
                    file_id = read_from_socket(sock, 16)
                    file_name = read_from_socket(sock, 100).strip(' ')
                    file_size = read_from_socket(sock, 10)
                    part_size = read_from_socket(sock, 6)
                    FilesManager.add_new_remote_file(file_name, file_id, file_size, part_size)
                    self.ui_handler.add_new_result_file(file_name, file_id, file_size, part_size)

            else:
                raise Exception("Response command error: %s. Wanted LOOK" % response)

        except Exception, ex:
            klog(str(ex))

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
        else:
            klog("LOGOUT not working correctly in directory")
        sock.close()
        return num_file_deleted

    def download_file(self, file_id):
        f = FilesManager.find_file_by_id(file_id)
        t = DownloadQueueThread(f, self, self.ui_handler)

    def download_part(self, peer_ip, peer_port, file_id, file_part):
        downloadSocket = connect_socket(peer_ip, peer_port)
        downloadSocket.send("RETP")
        downloadSocket.send(format_fileid(file_id))
        downloadSocket.send(format_partnum(file_part))
        # Star a thread that will take care of the download and of the socket management
        f = FilesManager.find_file_by_id(file_id)
        dlThread = DownloadThread(downloadSocket, f, peer_ip, self, self.ui_handler)
        dlThread.start()

    def register_part_to_tracker(self, file, part_num):
        my_tracker = UsersManager.get_tracker()
        sock = connect_socket(my_tracker.ip, my_tracker.port)
        local_ip = get_local_ip(sock.getsockname()[0])
        sock.send("RPAD" + UsersManager.get_my_session_id())
        sock.send(file.id)
        sock.send(format_partnum(part_num))

        try:
            response = read_from_socket(sock,4)
            if response == "APAD":
                part_num = read_from_socket(sock, 8)
                if part_num == file.numeropartichepossiedoperquestofile():
                    klog("Part succesfully registered")
                else:
                    klog("Wrong partnumber from directory")
            else:
                klog("Wrong ack received from directory service when trying to register a part")

        except Exception:
            klog("Exception in registering a downloaded part on the tracker")
        sock.close()

    def add_file_to_tracker(self, file):
        my_tracker = UsersManager.get_tracker()
        sock = connect_socket(my_tracker.ip, my_tracker.port)
        local_ip = get_local_ip(sock.getsockname()[0])
        sock.send("ADDR" + UsersManager.get_my_session_id())
        sock.send(file.id)
        sock.send(format_filesize(file.file_size))
        sock.send(format_partsize(file.part_size))
        sock.send(format_filename(file.filename))
        try:
            response = read_from_socket(sock, 4)
            if response == "AADR":
                part_num = read_from_socket(sock, 8)
                if int(part_num) == int(file.parts_count):
                    klog("File %s successfully added to directory service" % file.filename)
                else:
                    klog("Wrong partnumber received from directory")
            else:
                klog("wrong ack received from directory service")
        except Exception, ex:
            klog("Exception in adding file to tracker: %s" % str(ex))

    def add_all_files_to_tracker(self):
        for file in FilesManager.shared_files():
            self.add_file_to_tracker(file)

    def update_remote_file_data(self, file_id):
        my_tracker = UsersManager.get_tracker()
        try:
            sock = connect_socket(my_tracker.ip, my_tracker.port)
            local_ip = get_local_ip(sock.getsockname()[0])
            sock.send("FCHU" + UsersManager.get_my_session_id())
            sock.send(file_id)
            command = read_from_socket(sock, 4)
            if command == "AFCH":
                hitpeer = read_from_socket(sock, 3)
                for i in range(0, int(hitpeer)):
                    peer_ip = read_from_socket(sock, 15)
                    peer_port = read_from_socket(sock, 5)
                    f = FilesManager.find_file_by_id(file_id)

                    if not f:
                        raise Exception("File %s not found in request emitter" % file_id)

                    mask_length = int(math.ceil(f.parts_count / 8))
                    if f.parts_count % 8 != 0:
                        mask_length += 1
                    klog("MASK_LENGTH = %s" % mask_length)
                    partlist = read_from_socket(sock, mask_length)
                    partlist_array = []
                    for b in partlist:
                        byte = bin(int(binascii.b2a_hex(b),16))
                        byte = byte[2:]
                        byte = format_byte(byte)
                        for i in range(7,0, -1):
                            partlist_array.append(byte[i])
                    for j in range(len(partlist_array)):
                        #klog("%s PARTE %s: %s" %(file_id,j,partlist_array[j]))
                        FilesManager.update_remote_file_part(file_id, Peer(peer_ip, peer_port), j, bool(int(partlist_array[j])))
        except Exception, ex:
            klog("Exception in updating file data to tracker: %s" % str(ex))

