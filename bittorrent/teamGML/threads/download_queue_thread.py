__author__ = 'LucaFerrari MarcoBersani GiovanniLodi'

from threading import Thread
from custom_utils.logging import klog
from custom_utils.hashing import *
from custom_utils.sockets import read_from_socket
from PyQt4.QtCore import QThread, signal

DOWNLOAD_FOLDER = "downloads"
QUEUE_LENGTH = 5

class DownloadThread(QThread):

    def __init__(self, socket, filename, file_id, file_part, peer_ip, ui_handler):
        super(DownloadThread, self).__init__()
        self._socket = socket
        self._filename = filename
        self._file_id = file_id
        self._file_part = file_part
        self._peer_ip = peer_ip
        self._ui_handler = ui_handler

        klog("Started queue system for files %s %s" %(self._filename, str(self._file_id)))

    def _check_parts(self, file_id):
        pass

    def run(self):
        self.connect(self, SIGNAL("part_download_finished"), self._check_parts)
        parts = PartsManager.getPartsOrdered()
        for i in range(0, QUEUE_LENGTH):
            



        #TODO: infine ricostruisco il file.
