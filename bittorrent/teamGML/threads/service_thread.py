__author__ = 'LucaFerrari MarcoBersani GiovanniLodi'

from threading import Thread
import time
from managers.filesmanager import FilesManager
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

            #
            # PEERS
            #

            # Received package asking for a file
            if command == "RETP":
                klog("RETR received")
                CHUNK_DIM = 128

                md5 = encode_md5(self._socket.recv(16))

                self._socket.send("AREP")   #sending the ack command
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

            else:
                klog("ERROR: received a %s command that service_thread does not have to handle:" %command)
            # Close the socket
            self._socket.close()

        except Exception, ex:
            print ex

