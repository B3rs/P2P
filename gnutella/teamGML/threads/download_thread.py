__author__ = 'LucaFerrari MarcoBersani GiovanniLodi'

from threading import Thread
from custom_utils.logging import klog

class DownloadThread(Thread):

    CHUNK_DIM = 128

    def __init__(self, socket, filename, ui_handler):
        super(DownloadThread, self).__init__()
        self._socket = socket
        self._filename = filename
        self._ui_handler = ui_handler

    def file_size(self, path):
        file = open(path,'r')
        file.seek(0,2)
        size = F.tell()
        file.seek(0,0)
        file.close()
        return size

    def run(self):

        command = str(self._socket.recv(4))

        if command == "ARET":

            print "Download started"

            chunk_number = int(self._socket.recv(6))
            try:
                print "Download started"
                newFile = open(self._filename, "ab") # a = append, b = binary mode
                for i in range(0, chunk_number):
                    chunk_length = int(self._socket.recv(5))
                    chunk_data = self._socket.recv(chunk_length)
                    newFile.write(chunk_data)

                newFile.close()
                print "Download completed"

            except Exception:
                print "An exception has occurred"


        self._socket.close()
