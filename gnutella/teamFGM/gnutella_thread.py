__author__ = 'Frencina'

import gnutella_service

import socket # networking module
import threading

class Dispatcher(threading.Thread):

    def __init__(self, socketclient, addrclient, neighTable, pktTable):

        threading.Thread.__init__(self)

        # info sul peer che si connette, magari servono
        self.socketclient = socketclient
        self.addrclient = addrclient
        self.neighTable = neighTable
        self.pktTable = pktTable

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
        print request

        if request=="QUER":
            myservice = gnutella_service.Query(self.socketclient, self.addrclient, self.neighTable, self.pktTable)
            myservice.start()

        elif request=="AQUE":
            myservice = gnutella_service.AckQuery(self.socketclient, self.addrclient, self.neighTable, self.pktTable)
            myservice.start()

        elif request=="NEAR":
            myservice = gnutella_service.Near(self.socketclient, self.addrclient, self.neighTable, self.pktTable)
            myservice.start()

        elif request=="ANEA":
            myservice = gnutella_service.AckNear(self.socketclient, self.addrclient, self.neighTable, self.pktTable)
            myservice.start()

        elif request=="RETR":
            myservice = gnutella_service.Download(self.socketclient, self.addrclient, self.neighTable, self.pktTable)
            myservice.start()

        else:
            print "Errore nel pacchetto ricevuto"

    # end of run method

class ListenToPeers(threading.Thread):

    def __init__(self, my_IP, myP2P_port):

        #print "metodo init"

        threading.Thread.__init__(self)
        self.my_IP = my_IP
        self.myP2P_port = myP2P_port
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

    def gimmeNeigh(self, neighTable):

        self.neighTable = neighTable

    def gimmePkt(self, pktTable):

        self.pktTable = pktTable

    def run(self):

        self.address = (self.my_IP, self.myP2P_port)

        # Metto a disposizione una porta per il peer to peer
        self.peer_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.peer_socket.bind(self.address)
        self.peer_socket.listen(5) #socket per chi vorra' fare download da me

        a=0 #TODO debug

        while self.check == True:

            try:
                (SocketClient,AddrClient) = self.peer_socket.accept() # la accept restituisce la nuova socket del client connesso, e il suo indirizzo

                print "client " + AddrClient[0] + " connected"

                dispatcher = Dispatcher(SocketClient,AddrClient,self.neighTable,self.pktTable)
                dispatcher.start()

            except Exception,expt:
                a=a+1 #TODO debug



        self.peer_socket.close()