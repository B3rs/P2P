import socket # networking module
import sys
import threading
import time

from napster_client import NapsterClient

class DownloadMe(threading.Thread):

    def run(self):

        # PRINT DI PROVA -- TODO ELIMINARE
        while 1:
            (socketclient,address) = NapsterClient.peersocket.accept()

            #codice per gestire il download da parte dei peer
            #(meglio se concorrente)

