__author__ = 'GuiducciGrillandaLoPiccolo'

import gnutella_service

import socket # networking module
import threading
import time

class Dispatcher(threading.Thread):

    def __init__(self, socketclient, addrclient, my_IP_form, my_port_form):

        threading.Thread.__init__(self)

        # info sul peer che si connette, magari servono
        self.socketclient = socketclient
        self.addrclient = addrclient
        self.my_IP_form = my_IP_form
        self.my_port_form = my_port_form

    def sockread(self, socket, numToRead): #in ingresso ricevo la socket e il numero di byte da leggere

        lettiTot = socket.recv(numToRead)
        num = len(lettiTot)

        while (num < numToRead):
            letti = socket.recv(numToRead - num)
            num = num + len(letti)
            lettiTot = lettiTot + letti

        return lettiTot #restituisco la stringa letta
        # end of sockread method

    def filesize(self, n):

        ### calcolo della dimensione del file

        F = open(n,'r')
        F.seek(0,2)
        sz = F.tell()
        F.seek(0,0)
        F.close()
        return sz
        # end of filesize method

    def run(self):

        request = self.sockread(self.socketclient,4) #leggo i primi 4 byte per sapere cosa fare

        if request=="QUER":
            myservice = gnutella_service.Query(self.socketclient, self.addrclient, self.my_IP_form, self.my_port_form)
            myservice.start()

        elif request=="AQUE":
            myservice = gnutella_service.AckQuery(self.socketclient, self.addrclient, self.my_IP_form, self.my_port_form)
            myservice.start()

        elif request=="NEAR":
            myservice = gnutella_service.Near(self.socketclient, self.addrclient, self.my_IP_form, self.my_port_form)
            myservice.start()

        elif request=="ANEA":
            myservice = gnutella_service.AckNear(self.socketclient, self.addrclient, self.my_IP_form, self.my_port_form)
            myservice.start()

        elif request=="RETR":
            myservice = gnutella_service.Upload(self.socketclient, self.addrclient, self.my_IP_form, self.my_port_form)
            myservice.start()

        else:
            print "An error occured in packet received"

    # end of run method


class ListenToPeers(threading.Thread):

    def __init__(self, my_IP_form, my_port_form):

        #print "metodo init"

        threading.Thread.__init__(self)
        self.my_IP_form = my_IP_form
        self.my_port_form = my_port_form
        self.check = True

    def sockread(self, socket, numToRead): #in ingresso ricevo la socket e il numero di byte da leggere

        lettiTot = socket.recv(numToRead)
        num = len(lettiTot)

        while (num < numToRead):
            letti = socket.recv(numToRead - num)
            num = num + len(letti)
            lettiTot = lettiTot + letti

        return lettiTot #restituisco la stringa letta
        # end of sockread method

    def setCheck(self):
        self.check = False


    def run(self):


        self.address = (self.my_IP_form, int(self.my_port_form))

        # Metto a disposizione una porta per il peer to peer
        self.peer_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.peer_socket.bind(self.address)
        self.peer_socket.listen(5) #socket per chi vorra' fare download da me

        a=0 #TODO debug

        while self.check == True:

            try:
                (SocketClient,AddrClient) = self.peer_socket.accept() # la accept restituisce la nuova socket del client connesso, e il suo indirizzo

                #print "Peer " + AddrClient[0] + " connected"

                dispatcher = Dispatcher(SocketClient,AddrClient,self.my_IP_form,self.my_port_form)
                dispatcher.start()

            except Exception,expt:
                a=a+1 #TODO debug



        self.peer_socket.close()