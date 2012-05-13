__author__ = 'GuiducciGrillandaLoPiccolo'

import bittorrent_dir_serv

import socket # networking module
import threading

class Dispatcher(threading.Thread):

    def __init__(self, socketclient, addrclient, my_IP_form, dir_port_form):

        threading.Thread.__init__(self)

        # info sul peer che si connette, magari servono
        self.socketclient = socketclient
        self.addrclient = addrclient
        self.my_IP_form = my_IP_form
        self.dir_port_form = dir_port_form

    def sockread(self, socket, numToRead): #in ingresso ricevo la socket e il numero di byte da leggere

        lettiTot = socket.recv(numToRead)
        num = len(lettiTot)

        while (num < numToRead):
            letti = socket.recv(numToRead - num)
            num = num + len(letti)
            lettiTot = lettiTot + letti

        return lettiTot #restituisco la stringa letta
        # end of sockread method

    def run(self): #AGGIORNATO -- DA CONTROLLARE

        request = self.sockread(self.socketclient,4) #leggo i primi 4 byte per sapere cosa fare

        if request=="LOGI":
            myservice = bittorrent_dir_serv.Login(self.socketclient, self.addrclient, self.my_IP_form, self.dir_port_form)
            myservice.start()

        elif request=="LOGO":
            myservice = bittorrent_dir_serv.Logout(self.socketclient, self.addrclient, self.my_IP_form, self.dir_port_form)
            myservice.start()

        elif request=="ADFF":
            myservice = bittorrent_dir_serv.AddFile(self.socketclient, self.addrclient, self.my_IP_form, self.dir_port_form)
            myservice.start()

        elif request=="LOOK": #prima parte della ricerca
            myservice = bittorrent_dir_serv.LookFile(self.socketclient, self.addrclient, self.my_IP_form, self.dir_port_form)
            myservice.start()

        elif request=="FCHU": #seconda parte della ricerca
            myservice = bittorrent_dir_serv.FetchFile(self.socketclient, self.addrclient, self.my_IP_form, self.dir_port_form)
            myservice.start()

        elif request=="RPAD": #dopo il download
            myservice = bittorrent_dir_serv.PostDownload(self.socketclient, self.addrclient, self.my_IP_form, self.dir_port_form)
            myservice.start()

        else:
            print "Port 80: An error occured in packet received"

    # end of run method


class ListenToPeers(threading.Thread):

    def __init__(self, my_IP_form, dir_port_form):

        #print "metodo init"

        threading.Thread.__init__(self)
        self.my_IP_form = my_IP_form
        self.dir_port_form = dir_port_form

    def sockread(self, socket, numToRead): #in ingresso ricevo la socket e il numero di byte da leggere

        lettiTot = socket.recv(numToRead)
        num = len(lettiTot)

        while (num < numToRead):
            letti = socket.recv(numToRead - num)
            num = num + len(letti)
            lettiTot = lettiTot + letti

        return lettiTot #restituisco la stringa letta
        # end of sockread method



    def run(self):


        self.address = (self.my_IP_form, int(self.dir_port_form))

        # Metto a disposizione una porta per il peer to peer
        self.peer_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.peer_socket.bind(self.address)
        self.peer_socket.listen(5) #socket per chi vorra' fare download da me

        a=0 #debug

        while True:

            try:
                (SocketClient,AddrClient) = self.peer_socket.accept() # la accept restituisce la nuova socket del client connesso, e il suo indirizzo

                #print "Peer " + AddrClient[0] + " connected"

                dispatcher = Dispatcher(SocketClient,AddrClient,self.my_IP_form,self.dir_port_form)
                dispatcher.start()

            except Exception,expt:
                a=a+1 #debug


        self.peer_socket.close()