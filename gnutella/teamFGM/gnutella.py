__author__ = 'Frencina'

import gnutella_thread
import gnutella_service

import socket
import hashlib #per calcolare l'md5 dei file
import sys # mi consente di usare il metodo sys.stdout.write per scrivere sulla stessa riga
import copy
import string
import random
import time

class GnutellaPeer(object):

    def __init__(self):

        """
        This method set the program parameters, such as IPP2P:P2P to allow others connection from/to other peers
        and IP address of Centralized Directory
        """

        # PEER
        self.my_IP = socket.gethostbyname(socket.gethostname()) #brutto ma mi serve per ottenere il mio IP
        my_IP_split = self.my_IP.split(".")
        IP_1 = '%(#)03d' % {"#" : int(my_IP_split[0])}
        IP_2 = '%(#)03d' % {"#" : int(my_IP_split[1])}
        IP_3 = '%(#)03d' % {"#" : int(my_IP_split[2])}
        IP_4 = '%(#)03d' % {"#" : int(my_IP_split[3])}
        self.my_IP_form = IP_1 + "." + IP_2 + "." + IP_3 + "." + IP_4 #IP formattato per bene

        self.my_port = 6503 # porta che io rendo disponibile per altri peer quando vogliono fare download da me
        self.my_port_form = '%(#)05d' % {"#" : int(self.my_port)} #porta formattata per bene

        self.stop = False #non voglio uscire subito dal programma

        # CREO LA SOCKET PER GLI ALTRI PEERS
        self.myserver = gnutella_thread.ListenToPeers(self.my_IP_form, self.my_port_form)
        self.myserver.start()

        #vicini onnipresenti
        self.n1_IP = "192.168.0.187"
        self.n1_port = 6503
        #self.n2_IP = "192.168.0.187"
        #self.n2_port = 6503

        #tabella vicini
        neighService = gnutella_service.Service()
        print "Adding root #1"
        neighService.addNeighbour(self.n1_IP,self.n1_port)
        #print "Adding root #2"
        #neighService.addNeighbour(self.n2_IP,self.n2_port)

    # end of __init__ method

# Definition of auxiliary methods


    def generate_pktID(self):
        size=16
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.choice(chars) for x in range(size))
    #end of method generate_pktID

    def sockread(self, socket, numToRead): #in ingresso ricevo la socket e il numero di byte da leggere

        lettiTot = socket.recv(numToRead)
        num = len(lettiTot)

        while (num < numToRead):
            letti = socket.recv(numToRead - num)
            num = num + len(letti)
            lettiTot = lettiTot + letti

        return lettiTot #restituisco la stringa letta
    # end of sockread method

    def openConn(self, IP, port):
        #mi connetto al vicino
        neigh_addr = (IP, int(port))
        try:
            #print "Connecting with Neighbour " + IP #TODO debug
            neigh_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            neigh_socket.connect(neigh_addr)
        except IOError, expt: #IOError exception includes a sub-exception socket.error
            print "Error occured in Connection with neighbour -> %s" % expt + "\n"
        else:
            return neigh_socket
    # end of method openConn


    def closeConn(self, socket):
        #mi disconnetto dal vicino
        try:
            socket.close()
        except IOError, expt: #IOError exception includes a sub-exception socket.error
            print "Error occured in Disconnection with neighbour -> %s" % expt + "\n"
    # end of method closeConn


    def findNeigh(self):

        print "Find neighbours..."

        neigh_TTL = "0" #inizializzazione fittizia per il while di conttollo stdin
        while int(neigh_TTL) < 1: #verifico che non venga inserito un valore non possibile
            neigh_TTL = raw_input("Insert neighbours TTL (min=1, typ=2): ")
        neigh_TTL_form = '%(#)02d' % {"#" : int(neigh_TTL)}
        pktID =  self.generate_pktID()

        nearService = gnutella_service.Service()

        myQueryTable = nearService.getMyQueryTable()
        new_entry = []
        new_entry.append(pktID)
        new_entry.append(time.time())
        myQueryTable.append(new_entry)
        nearService.setMyQueryTable(myQueryTable)

        # invio la richiesta di query flooding a tutti i miei vicini

        neighTable = nearService.getNeighTable()
        for n in range(0,len(neighTable)):
            neigh_sock = self.openConn(neighTable[n][0], neighTable[n][1]) #passo ip e porta
            neigh_sock.sendall("NEAR" + pktID + self.my_IP_form + self.my_port_form + neigh_TTL_form)
            print "invio NEAR" + str(pktID) + self.my_IP_form + str(self.my_port_form) + neigh_TTL_form
            self.closeConn(neigh_sock)

    # end of findNeigh method


    def findFile(self):

        print "Find files...\n"

        query_TTL = "0" #inizializzazione fittizia per il while di controllo stdin
        search = raw_input("Insert a search string: ")
        search_form = '%(#)020s' % {"#" : search} #formatto la stringa di ricerca
        while int(query_TTL) < 1 :
            query_TTL = raw_input("Insert TTL for query request (min=1, typ=4 or 5): ")
        query_TTL_form = '%(#)02d' % {"#" : int(query_TTL)}
        pktID = self.generate_pktID()

        querService = gnutella_service.Service()

        myQueryTable = querService.getMyQueryTable()
        new_entry = []
        new_entry.append(pktID)
        new_entry.append(time.time())
        myQueryTable.append(new_entry)
        querService.setMyQueryTable(myQueryTable)

        # invio la richiesta di query flooding a tutti i miei vicini
        neighTable = querService.getNeighTable()
        for n in range(0,len(neighTable)):
            neigh_sock = self.openConn(neighTable[n][0], neighTable[n][1]) #passo ip e porta
            neigh_sock.sendall("QUER" + pktID + self.my_IP_form + self.my_port_form + query_TTL_form + search_form)
            print "invio QUER" + str(pktID) + self.my_IP_form + str(self.my_port_form) + query_TTL_form + search_form
            self.closeConn(neigh_sock)

    # end of findFile method


    def download(self):

        print "Download..."

        id = raw_input("Choose an identification: ")

        downService = gnutella_service.Service()
        downTable = downService.getDownTable()
        for i in range(0,len(downTable)):
            if int(id) == downTable[i][0]:
                filemd5 = downTable[i][3]
                filename = downTable[i][4]
                pktid = downTable[i][5]
                row = i

        queryTable = downService.getMyQueryTable()

        for i in range(0,len(queryTable)):

            if pktid == queryTable[i][0]:

                old_time = queryTable[i][1] #per ripristinarlo in caso di fallito download
                queryTable[i][1] = 1.0 #setto il tempo a 1 per dire che e' un tempo molto vecchio

        downService.setMyQueryTable(queryTable)


        #apro una socket verso il peer da cui devo scaricare
        #"iodown" perche' io faccio il download da lui

        try: # e' necessario tenere sotto controllo la connessione, perche' puo' disconnettersi il peer o non essere disponibile

            iodown_socket = self.openConn(downTable[row][1], int(downTable[row][2])) #passo ip e porta
        except IOError: #IOError exception includes socket.error
            print "Connection with " + iodown_host + "not available"
        else:
            print "Connection with peer enstablished.\n"

            # SPEDISCO IL PRIMO MESSAGGIO
            iodown_socket.sendall("RETR" + filemd5)

            try:
                # Acknowledge "ARET" dal peer
                ack = self.sockread(iodown_socket, 10)
            except IOError:
                print "Connection error. The peer " + iodown_host + " is death\n"
            else:

                if ack[:4]=="ARET":

                    #print "Download incoming..."

                    #pulisco il filename dagli spazi vuoti
                    filename_clean=str(filename).strip(' ')

                    fout = open(filename_clean,"ab") #a di append, b di binary mode

                    num_chunk = ack[4:10]

                    #pulisco il numero di chunks dagli 0
                    num_chunk_clean = str(num_chunk).lstrip('0')

                    #print "The number of chunks is " + num_chunk_clean + "\n"

                    for i in range (0,int(num_chunk_clean)): #i e' il numero di chunk

                        #print "Watching chunk number " + str(int(i+1))

                        #devo leggere altri byte ora
                        #ne leggo 5 perche' 5 sono quelli che mi diranno poi quanto e' lungo il chunk
                        try:

                            lungh_form = self.sockread(iodown_socket, 5) #ricevo lunghezza chunck formattata
                            #print lungh_form

                            lungh = int(lungh_form) #converto in intero
                            #print lungh

                            #devo leggere altri byte ora
                            #ne leggo lungh perche' quella e' proprio la lunghezza del chunk

                            #data = iodown_socket.recv(lungh)
                            data = self.sockread(iodown_socket, lungh)
                            #print "ho ricevuto i byte" #TODO debug mode

                            #lo devo mettere sul mio file che ho nel mio pc

                            fout.write(data) #scrivo sul file in append

                            #print ""

                        except IOError, expt:

                            print "Connection or File-access error -> %s" % expt

                            print "\nDownload failed"

                            queryTable = downService.getMyQueryTable()

                            for i in range(0,len(queryTable)):

                                if pktid == queryTable[i][0]:

                                    queryTable[i][1] = old_time #ripristino il tempo vecchio per download fallito

                            downService.setMyQueryTable(queryTable)

                            break
                        #ho finito di ricevere il file

                    fout.close() #chiudo il file perche' ho finito di scaricarlo

                    self.closeConn(iodown_socket) #chiudo la socket verso il peer da cui ho scaricato


    def goOut(self):
        gp.stop=True
        self.myserver.setCheck()
        print "You're about exiting from P2P network"


    def error(self):
        print "Option not valid: try again!\n"
    # end of error method



    def doYourStuff(self):

        """
        This methods allow user to navigate into menu
        """

        print "Choose between the following options, typing the number:\n"

        print "1. Find neighbours"
        print "2. Search file"
        print "3. Download file"
        print "4. Exit program\n"

        choice = raw_input("Choose an option: ")

        opt = {

            '1' : self.findNeigh,
            '2' : self.findFile,
            '3' : self.download,
            '4' : self.goOut

        }

        print ""

        opt.get(choice,self.error)() #se l'utente ha digitato un qualcosa che non esiste, viene chiamata error()

    # end of doYourStuff method



if __name__ == "__main__":

    gp = GnutellaPeer() #inizializzazione

    while not gp.stop:

        gp.doYourStuff() #stampa del menu ed esecuzione dell'operazione scelta