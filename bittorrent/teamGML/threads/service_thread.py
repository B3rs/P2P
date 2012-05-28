__author__ = 'LucaFerrari MarcoBersani GiovanniLodi'

from threading import Thread

from managers.filesmanager import FilesManager
from managers.usersmanager import UsersManager
from custom_utils.formatting import *
from custom_utils.files import file_size
from custom_utils.logging import klog


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
                klog("RETP received")
                CHUNK_DIM = 128

                file_id = self._socket.recv(16)
                part_num = self._socket.recv(8)

                self._socket.send("AREP")   #sending the ack command
                remote_ip = self._socket.getpeername()[0]
                my_session_id = UsersManager.get_my_session_id()

                # Get the file matching the file_id
                klog("finding file with id: %s, session_id %s, part %s" %(file_id, my_session_id, part_num))

                file = FilesManager.find_shared_file_by_id(file_id)

                if file:
                    klog("i have found the file: %s stored in %s" % (file.filename, file.filepath))

                    # Chunks
                    size = file.get_part_size(part_num)#file_size(file.filepath)
                    bytes_sent = 0
                    chunks_num = int(size // CHUNK_DIM)
                    leftover = size % CHUNK_DIM
                    if leftover != 0.0:
                        chunks_num += 1

                    self._socket.send(format_chunks_number(chunks_num)) #sending the chunks number

                    part = file.get_part(part_num)
                    part_size = file.get_part_size(part_num)

                    index = 0
                    chunk = part[0:CHUNK_DIM]

                    while True:
                        self._socket.send(format_chunk_length(len(chunk)))  #sending the chunk length
                        bytes_sent += self._socket.send(chunk)    #sending the chunk

                        percent = bytes_sent*100/size
                        self.ui_handler.upload_file_changed(file.filename, file.id, part_num, remote_ip, percent)

                        index += 1
                        if ((index * CHUNK_DIM) <= part_size) and ((index + 1)* CHUNK_DIM <= part_size):
                            chunk = part[index * CHUNK_DIM : (index + 1)* CHUNK_DIM]
                        elif ((index * CHUNK_DIM) <= part_size) and ((index + 1)* CHUNK_DIM > part_size):
                            chunk = part[index * CHUNK_DIM : ]
                        else:
                            break

                    '''
                    #open the file
                    file2send = file.get_part(part_num)#open(file.filepath, 'rb')
                    chunk = file2send.read(CHUNK_DIM)

                    while chunk != '':
                        self._socket.send(format_chunk_length(len(chunk)))  #sending the chunk length
                        bytes_sent += self._socket.send(chunk)    #sending the chunk

                        percent = bytes_sent*100/size
                        self.ui_handler.upload_file_changed(file.filename, file.id, part_num, remote_ip, percent)

                        chunk = file2send.read(CHUNK_DIM)
                    file2send.close()
                    '''
                    klog("upload completed: %s" %file.filename)
                    self.ui_handler.upload_file_changed(file.filename, file.id, part_num, remote_ip, 100)

                else:
                    klog("I do not have this file!")

            else:
                klog("ERROR: received a %s command that service_thread does not have to handle:" %command)
            # Close the socket
            self._socket.close()

        except Exception, ex:
            print ex

