__author__ = 'LucaFerrari MarcoBersani GiovanniLodi'

from threading import Timer
from custom_utils.logging import klog
from PyQt4.QtCore import SIGNAL, QObject
from managers.filesmanager import FilesManager
import random


DOWNLOAD_FOLDER = "downloads"
QUEUE_LENGTH = 5

class DownloadQueue(QObject):

    def __init__(self, file, request_emitter, ui_handler):
        super(DownloadQueue, self).__init__()
        self._file = file
        self._ui_handler = ui_handler
        self._request_emitter = request_emitter
        self._downloaded_parts = FilesManager.get_completed_file_parts_nums(file.id)


        klog("Started queue system for files %s %s" %(self._file.filename, str(self._file.id)))

        self.connect(self, SIGNAL("part_download_finished"), self._completed_part)
        self._check_parts()
        parts = FilesManager.get_ordered_parts_number(self._file.id)
        for i in range(min(QUEUE_LENGTH, len(parts))):
            peers = FilesManager.get_peers_for_file_part(self._file.id, parts[i])
            if len(peers) > 0:
                if len(peers) == 1:
                    peer = peers[0]
                else:
                    peer = peers[random.randrange(0,len(peers)-1)]
                self._request_emitter.download_part(peer.ip, peer.port, self._file.id, parts[i])

    def _completed_part(self, file_id, part_num):

        if str(file_id) != str(self._file.id):
            return

        part_num = int(part_num)

        klog("Completed part %d" %part_num)

        if part_num not in self._downloaded_parts:
            self._downloaded_parts.append(part_num)


        if len(self._downloaded_parts) == self._file.parts_count:
            klog("All parts downloaded, creating the file")
            self._timer.cancel()
            FilesManager.create_file_from_parts(self._file.id)
        else:
            klog("Starting the new part")

            parts = FilesManager.get_ordered_parts_number(self._file.id)
            if len(parts) >0:
                peers = FilesManager.get_peers_for_file_part(self._file.id, parts[0])

                if len(peers) > 0:
                    if len(peers) > 1:
                        peer = peers[random.randrange(0,len(peers)-1)]
                    else:
                        peer = peers[0]

                    self._request_emitter.download_part(peer.ip, peer.port, file_id, parts[0])
                    klog("Started download part %d from peer: %s" %(parts[0], peer.ip))
    
    def _check_parts(self):
        klog("Timer: update remote file datas for file: %s" %self._file.id)
        self._request_emitter.update_remote_file_data(self._file.id)
        self._timer = Timer(60,self._check_parts, ())
        self._timer.start()
