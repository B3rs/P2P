__author__ = 'LucaFerrari MarcoBersani GiovanniLodi'

from threading import Thread
from custom_utils.logging import klog
from custom_utils.hashing import *
from custom_utils.sockets import read_from_socket

DOWNLOAD_FOLDER = "downloads"

class DownloadThread(Thread):

    def __init__(self, socket, filename, file_md5, peer_ip, ui_handler):
        super(DownloadThread, self).__init__()
        self._socket = socket
        self._filename = filename
        self._file_md5 = file_md5
        self._peer_ip = peer_ip
        self._ui_handler = ui_handler

        klog("downloading %s %s" %(self._filename, str(self._file_md5)))

    def run(self):

        command = str(read_from_socket(self._socket, 4))

        if command == "AREP":

            klog("Received AREP")

            chunk_number = int(read_from_socket(self._socket, 6))
            try:
                klog("Download started")
                klog("chunk number: " + str(chunk_number))
                newFile = open(DOWNLOAD_FOLDER+"/"+self._filename, "wb") # a = append, b = binary mode

                for i in range(0, chunk_number):
                    chunk_length = read_from_socket(self._socket, 5)
                    chunk_length = int(chunk_length)

                    chunk_data = read_from_socket(self._socket, chunk_length)
                    newFile.write(chunk_data)

                    percent = i* 100/chunk_number
                    self._ui_handler.download_file_changed(self._filename, self._file_md5, self._peer_ip, percent)

                newFile.close()
                self._ui_handler.download_file_changed(self._filename, self._file_md5, self._peer_ip, 100)
                klog("Download completed")
                klog("TODO: send RPAD to directory ")
                klog("TODO: receive APAD from directory")

            except Exception, ex:
                klog("An exception has occurred: "+str(ex))


        self._socket.close()
