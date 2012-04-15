__author__ = 'LucaFerrari MarcoBersani GiovanniLodi'

from threading import Thread
from custom_utils.logging import klog
from custom_utils.hashing import *

DOWNLOAD_FOLDER = "../downloads"

class DownloadThread(Thread):

    CHUNK_DIM = 128

    def __init__(self, socket, filename, file_md5, peer_ip, ui_handler):
        super(DownloadThread, self).__init__()
        self._socket = socket
        self._filename = filename
        self._file_md5 = file_md5
        self._peer_ip = peer_ip
        self._ui_handler = ui_handler

        print "md5: " + encode_md5(file_md5)

    def run(self):

        command = str(self._socket.recv(4))

        if command == "ARET":

            print "Received ARET"

            chunk_number = int(self._socket.recv(6))
            try:
                print "Download started"
                print "chunk number: " + str(chunk_number)
                newFile = open(DOWNLOAD_FOLDER+"/"+self._filename, "wb") # a = append, b = binary mode

                for i in range(0, chunk_number):
                    print "i: "+str(i)

                    chunk_length = self._socket.recv(5)
                    print chunk_length
                    chunk_length = int(chunk_length)

                    chunk_data = self._socket.recv(chunk_length)
                    newFile.write(chunk_data)

                    #percent = i* 100/chunk_number
                    #self._ui_handler.download_file_changed(self._filename, self._file_md5, self._peer_ip, percent)

                newFile.close()
                print "Download completed"

            except Exception, ex:
                print "An exception has occurred: "+str(ex)


        self._socket.close()
