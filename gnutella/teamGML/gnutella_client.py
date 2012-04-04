__author__ = 'LucaFerrari MarcoBersani GiovanniLodi'

from managers.filesmanager import FilesManager
from models.peer import Peer
import socket, os, sys
from threading import Thread
from custom_utils.logging import klog
from custom_utils.hashing import decode_md5, encode_md5, calculate_md5_for_file_path

from threads.background_thread import BackgroundThread
from threads.ui_thread import UIThread


class GnutellaPeer(object):

    def __init__(self):
        # Error checking
        if len(sys.argv) < 3:
            print "Usage $ python gnutella ip port"
            sys.exit()

        self.ip = sys.argv[1]
        self.port = sys.argv[2]


    def start(self):
        print "Gnutella started on %s:%s" %(self.ip, self.port)

        # Launch background thread for network handling
        bg = BackgroundThread(self.ip, self.port)
        bg.setDaemon(True)
        bg.start()

        # Launch ui thread for interaction with the user
        ui = UIThread()
        ui.start()


if __name__ == "__main__":
    ns = GnutellaPeer()
    ns.start()


