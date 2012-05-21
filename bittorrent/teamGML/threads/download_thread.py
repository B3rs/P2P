__author__ = 'LucaFerrari MarcoBersani GiovanniLodi'

from threading import Thread
from custom_utils.logging import klog
from custom_utils.hashing import *
from custom_utils.sockets import read_from_socket
from managers.filesmanager import FilesManager
from PyQt4.QtCore import QThread, SIGNAL

DOWNLOAD_FOLDER = "downloads"

class DownloadThread(QThread):

    def __init__(self, socket, filename, file_id, file_part, peer_ip, request_emitter, ui_handler, queue):
        super(DownloadThread, self).__init__()
        self._socket = socket
        self._filename = filename
        self._file_id = file_id
        self._file_part = file_part
        self._peer_ip = peer_ip
        self._ui_handler = ui_handler
        self._request_emitter = request_emitter
        self._queue = queue

        klog("downloading %s %s" %(self._filename, str(self._file_id)))

    def run(self):

        command = str(read_from_socket(self._socket, 4))

        if command == "AREP":

            klog("Received AREP")

            chunk_number = int(read_from_socket(self._socket, 6))
            try:
                klog("Download started")
                FilesManager.set_status_part_for_file(self._file_id, self._file_part, "downloading")
                klog("chunk number: " + str(chunk_number))
                newFile = open(FilesManager.get_filepart_path_from_file(), "wb") # a = append, b = binary mode

                for i in range(0, chunk_number):
                    chunk_length = read_from_socket(self._socket, 5)
                    chunk_length = int(chunk_length)

                    chunk_data = read_from_socket(self._socket, chunk_length)
                    newFile.write(chunk_data)

                    percent = i* 100/chunk_number
                    self._ui_handler.download_file_changed(self._filename, self._file_id, self._peer_ip, percent)

                newFile.close()
                self._ui_handler.download_file_changed(self._filename, self._file_id, self._peer_ip, 100)
                klog("Download completed")

                f = FilesManager.find_file_by_id(self._file_id)

                self._request_emitter.register_part_to_tracker(f, self._file_part)

            except Exception, ex:
                klog("An exception has occurred: "+str(ex))


        self._socket.close()

        self.emit(SIGNAL("part_download_finished"), self._file_id, self._file_part)

