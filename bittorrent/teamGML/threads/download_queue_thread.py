__author__ = 'LucaFerrari MarcoBersani GiovanniLodi'

from threading import Thread
from custom_utils.logging import klog
from custom_utils.hashing import *
from custom_utils.sockets import *
from PyQt4.QtCore import QThread, SIGNAL
from managers.filesmanager import FilesManager
from threads.download_thread import DownloadThread
from threads.request_emitter import RequestEmitter
import random


DOWNLOAD_FOLDER = "downloads"
QUEUE_LENGTH = 5

class DownloadQueueThread(QThread):

    def __init__(self, socket, file, peer_ip, ui_handler):
        super(DownloadQueueThread, self).__init__()
        self._socket = socket
        self._file = file
        self._peer_ip = peer_ip
        self._ui_handler = ui_handler
        self._downloaded_parts = 0
        klog("TODO caricare qui le eventuali parti già scaricate")


        klog("Started queue system for files %s %s" %(self._file.filename, str(self._file.id)))

    def _completed_part(self, file_id, file_part):
        if file_id != self._file.id:
            return
        self._downloaded_parts += 1
        if self._downloaded_parts == self._file.parts_count:
            klog("TODO ricomporre il file")
        else:
            klog("Part finished, starting the new part")

            parts = FilesManager.get_ordered_parts_number()
            peers = FilesManager.get_peers_for_file_part(parts[0])
            peer = peers[random.randrange(0,len(peers)-1)]
            RequestEmitter.download_part(peer.ip, peer.port, file_id, parts[0], self._file.filename)



    def run(self):
        self.connect(self, SIGNAL("part_download_finished"), self._downloaded_parts)
        parts = FilesManager.get_ordered_parts_number()
        for i in range(0, min(QUEUE_LENGTH, len(parts))):
            peers = FilesManager.get_peers_for_file_part()
            peer = None
            if len(peers) > 0:
                peer = peers[random.randrange(0,len(peers)-1)]
                RequestEmitter.download_part(peer.ip, peer.port, self._file.id, parts[i], self._file.filename)
