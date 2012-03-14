from twisted.internet import address

__author__ = 'ingiulio'

import socket # networking module
import sys
import threading
import time
import os
from napster_client import NapsterClient #TODO controllare

class ListenToPeers(threading.Thread):


    def run(self, my_IP, myP2P_port):

    # Metto a disposizione una porta per il peer to peer
        self.peer_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.peer_socket.bind(my_IP,myP2P_port)
        self.peer_socket.listen(100) #socket per chi vorra' fare download da me

        while 1:

            # entro nel while con la socket ("peer_socket") gia' in listen
            # voglio far partire un thread per ogni accept che ricevo

            (SocketClient,AddrClient) = NapsterClient.peer_socket.accept() # la accept restituisce la nuova socket del client connesso, e il suo indirizzo

            print "il client " + address[0] + " si e' connesso"

            peer=PeerHandler(SocketClient,AddrClient)
            peer.start()


class PeerHandler(threading.Thread):


    def __init__(self, socketclient, addrclient):

        # info sul peer che si connette, magari servono
        self.socketclient = socketclient
        self.addrclient = addrclient

    def filesize(n):

        ### calcolo della dimensione del file

        F = open(n,'r')
        F.seek(0,2)
        sz = F.tell()
        F.seek(0,0)
        F.close()
        return sz

    def run(self):

        print "Sono un thread che si occupa di un altro peer"

        chunk_dim = 128 # specifica la dimensione in byte del chunk (fix)

        # mi metto in receive della string "RETR"
        request = self.socketclient.recv(20)
        if request[:4] == "RETR":
            print "ok, mi hai chiesto il file, controllo l'md5"

            md5tofind = request[4:20]

            # ricerca della corrispondenza
            for i in NapsterClient.fileTable:
                if (NapsterClient.fileTable[i[1]])== md5tofind:
                    print "trovato file!"
                    filename = NapsterClient.fileTable[i[0]]


            # dividere il file in chuncks

            try :
                file = open(filename, "rb")
            except Exception,expt:
                print "Error: %s" %expt + "\n"
                print "An error occured, file upload unavailable for peer " + self.addrclient[0] + "\n"
            else :
                tot_dim=filesize(filename)
                num_of_chunks = int(tot_dim // chunk_dim) #risultato intero della divisione
                resto = tot_dim % chunk_dim #eventuale resto della divisione
                if resto != 0.0:
                    num_of_chunks+=1

                num_chunks_form = '%(#)06d' % {"#" : int(num_of_chunks)}
                file.seek(0,0) #sposto la testina di lettura ad inizio file
                try :
                    buff = file.read(chunk_dim)
                    chunk_sent = 0
                    ListenToPeers.peer_socket.send("ARET" + num_chunks_form)
                    while len(buff) == chunk_dim :
                        chunk_dim_form = '%(#)05d' % {"#" : len(buff)}
                        try:
                            ListenToPeers.peer_socket.send(chunk_dim_form + buff)
                        except IOError: #this exception includes the socket.error child!
                            print "Connection error due to the death of your peer!!!\n"
                            raise ConnException
                        else:
                            chunk_sent = chunk_sent +1
                            print "Sent " + chunk_sent + " chunks to " + self.addrclient[0] #TODO debug
                            buff = file.read(chunk_dim)
                    if len(buff) != 0:
                        chunk_last_form = '%(#)05d' % {"#" : len(buff)}
                        ListenToPeers.peer_socket.send(chunk_last_form + buff)

                except EOFError:
                    print "You have read a EOF char"
                except ConnException:
                    print "Your friend is a bad peer, and a bad developer!\n"

                else :
                    print "End of upload to "+self.addrclient[0]+ " of "+filename
                    file.close()
        else:
            print "ack parsing failed, for RETR\n"
        
