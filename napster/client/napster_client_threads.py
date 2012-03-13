__author__ = 'ingiulio'

import socket # networking module
import sys
import threading
import time
from napster_client import NapsterClient

class ListenToPeers(threading.Thread):


    def run(self, my_IP, myP2P_port):

    # Metto a disposizione una porta per il peer to peer
        self.peer_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.peer_socket.bind(my_IP,myP2P_port)
        self.peer_socket.listen(100) #socket per chi vorra' fare download da me

        while 1:

            # entro nel while con la socket ("peer_socket") già in listen
            # voglio far partire un thread per ogni accept che ricevo

            (SocketClient,AddrClient) = NapsterClient.peer_socket.accept() # la accept restituisce la nuova socket del client connesso, e il suo indirizzo

            peer=PeerHandler(SocketClient,AddrClient)
            peer.start()


class PeerHandler(threading.Thread):


    def __init__(self, socketclient, addrclient):

        # info sul peer che si connette, magari servono
        self.socketclient = socketclient
        self.addrclient = addrclient

    def run(self):

        print "Sono un thread che si occupa di un altro peer"

        # mi metto in receive della string "RETR"
        request = self.socketclient.rcv()
        if request[:4] == "RETR":
            print "ok, mi hai chiesto il file, controllo l'md5"

            md5tofind = request[4:20] #TODO va bene così o mi arriva formattato?

            # ricerca della corrispondenza
            for i in NapsterClient.fileTable:
                if (NapsterClient.fileTable[i[1]])== md5tofind:
                    print "trovato file!"
                    filename = NapsterClient.fileTable[i[0]]

            # TODO
            # dividere il file in chuncks
            file = open(filename)
            file.seek(0,0)
            buff = file.read(128)
            chunk_sent = 0
            while len(buff) == 128 :
                ListenToPeers.peer_socket.send(buff)
                chunk_sent = chunk_sent +1
                print "Sent " + chunk_sent + " chunks"
                file.seek(1,128)
                buff = file.read(128)
            ListenToPeers.peer_socket.send(buff)

            print "End of upload"

            # inviare risposta al client
            # registrare sulla directory il download
            self.socketclient.send()

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



