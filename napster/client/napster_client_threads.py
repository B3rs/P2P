__author__ = 'ingiulio'

import socket # networking module
import sys
import threading
import time

class DownloadMe(threading.Thread):

    def run(self):

        while 1:
            (socketclient,address) = NapsterClient.peer_socket.accept()

            #codice per gestire il download da parte dei peer
            #(meglio se concorrente)
            # un peer si attacca a me e mi manda una stringa fatta cosi' RETR[4B].Filemd5[16B]
            # io devo leggerla e parsarla
            # e poi devo andare a recuperare il file che ha quel md5
            # mi sa che per far cio' dovrei mantenermi una tabellina in cui mi scrivo la corrispondenza tra
            # i nomi dei file che uploado e i loro md5 (altrimenti come posso fare? parlarne insieme)
            # quando ho recuperato il file lo devo mandare al peer in questo modo:
            # ARET[4B].#chunk[6B].{Lenchunk_i[5B].data[LB]}(i=1..#chunk)
            # decidendo io il numero dei chunk e la loro lunghezza
            # poi basta, non devo fare nient'altro