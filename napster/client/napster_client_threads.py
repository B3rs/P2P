__author__ = 'ingiulio'

import socket # networking module
import threading

class ListenToPeers(threading.Thread):

    def __init__(self, my_IP, myP2P_port):

        print "metodo init"

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

    def gimmeFile(self, fileTable):

        self.fileTable = fileTable

    def setCheck(self):
        self.check = False

    def run(self):

        print "ListentoPeers Run method" #TODO debug
        self.address = (self.my_IP, self.myP2P_port)

        # Metto a disposizione una porta per il peer to peer
        self.peer_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        print "creata peer socket" #TODO debug
        self.peer_socket.bind(self.address)
        print "ho fatto il bind"
        self.peer_socket.listen(100) #socket per chi vorra' fare download da me
        print "in ascolto del peer"

        a=0

        while self.check == True:

            # entro nel while con la socket ("peer_socket") gia' in listen
            # voglio far partire un thread per ogni accept che ricevo

            self.peer_socket.settimeout(5.0)

            try:
                (SocketClient,AddrClient) = self.peer_socket.accept() # la accept restituisce la nuova socket del client connesso, e il suo indirizzo

                print "il client " + self.address[0] + " si e' connesso"

                peer = PeerHandler(SocketClient,AddrClient,self.fileTable)
                peer.start()

            except Exception,expt:
                a=a+1



        self.peer_socket.close()


class PeerHandler(threading.Thread):


    def __init__(self, socketclient, addrclient, fileTable):

        threading.Thread.__init__(self)

        # info sul peer che si connette, magari servono
        self.socketclient = socketclient
        self.addrclient = addrclient
        self.fileTable = fileTable

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

        print "Sono un thread che si occupa di un altro peer"

        chunk_dim = 128 # specifica la dimensione in byte del chunk (fix)

        # mi metto in receive della string "RETR"
        #request = self.socketclient.recv(20)
        request = self.sockread(self.socketclient, 20)

        if request[:4] == "RETR":
            print "ok, mi hai chiesto il file, controllo l'md5"

            md5tofind = request[4:20]

            # ricerca della corrispondenza
            for i in self.fileTable:
                print "md5 " + i[1]
                print "filename " + i[0]
                if i[1] == md5tofind:
                    print "file found!"
                    filename = i[0]
                    print filename


            # dividere il file in chuncks

            try :
                file = open(filename, "rb")
            except Exception,expt:
                print "Error: %s" %expt + "\n"
                print "An error occured, file upload unavailable for peer " + self.addrclient[0] + "\n"
            else :
                tot_dim=self.filesize(filename)
                num_of_chunks = int(tot_dim // chunk_dim) #risultato intero della divisione
                resto = tot_dim % chunk_dim #eventuale resto della divisione
                if resto != 0.0:
                    num_of_chunks+=1

                num_chunks_form = '%(#)06d' % {"#" : int(num_of_chunks)}
                file.seek(0,0) #sposto la testina di lettura ad inizio file
                try :
                    buff = file.read(chunk_dim)
                    chunk_sent = 0
                    self.socketclient.sendall("ARET" + num_chunks_form)
                    while len(buff) == chunk_dim :
                        chunk_dim_form = '%(#)05d' % {"#" : len(buff)}
                        try:

                            print chunk_dim_form
                            self.socketclient.sendall(str(chunk_dim_form) + buff)
                            chunk_sent = chunk_sent +1
                            print "Sent " + str(chunk_sent) + " chunks to " + str(self.addrclient[0])#TODO debug
                            buff = file.read(chunk_dim)
                        except IOError: #this exception includes the socket.error child!
                            print "Connection error due to the death of the peer!!!\n"
                    if len(buff) != 0:
                        print "coda del file" #TODO debug
                        chunk_last_form = '%(#)05d' % {"#" : len(buff)}
                        self.socketclient.sendall(chunk_last_form + buff)
                    print "End of upload to "+self.addrclient[0]+ " of "+filename
                    file.close()
                    print "ho chiuso il file" #TODO debug
                except EOFError:
                    print "You have read a EOF char"
        else:
            print "ack parsing failed, for RETR\n"
        self.socketclient.close()
        #ListenToPeers.inService = False

    # end of run method