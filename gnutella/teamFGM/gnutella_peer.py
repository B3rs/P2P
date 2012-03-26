__author__ = 'ingiulio'

import socket
import hashlib #per calcolare l'md5 dei file
import time # per le funzioni di wait -> uso le sleep, che mi freezano il processo
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
        #self.myserver = gnutella_peer_threads.ListenToPeers(self.my_IP, self.my_port)
        #self.myserver.start()

        #vicini onnipresenti
        self.n1_IP = "0.0.0.0"
        self.n1_port = 9999
        self.n2_IP = "0.0.0.0"
        self.n2_port = 9999

        #tabelle varie
        self.dim_neighTable = 3 #dimensione massima della tabella
        self.neighTable = [dim_neighTable]
        self.pktTable = []
        #eventualmente aggiungere tabella con i file

        #li vado a mettere dentro a neighTable
        self.addNeighbour(self.n1_IP,self.n1_port)
        self.addNeighbour(self.n2_IP,self.n2_port)

    # end of __init__ method

# Definition of auxiliary methods


    def dots(self):
        """
        this silly method print the sequence ... after a sentence
        """
        i = 0
        while i<3:
            sys.stdout.write(".")
            time.sleep(0.5)
            i = i + 1
    # end of method dots

    def md5_for_file(self,fileName):

        """
        md5_for_file method get md5 checksum from a fileName given as parameter in function call
        """
        #print "Funzione che calcola l'md5 di un file" #TODO: DEBUG MODE

        try:
            f = open(fileName)
        except Exception, expt:
            print "Error: %s" % expt
        else :
            md5 = hashlib.md5()
            while True:
                data = f.read(128)
                if not data:
                    break
                md5.update(data)
            #print md5.digest()
            return md5.digest()
    # end of md5_for_file method

    def sockread(self, socket, numToRead): #in ingresso ricevo la socket e il numero di byte da leggere

        lettiTot = socket.recv(numToRead)
        num = len(lettiTot)

        while (num < numToRead):
            letti = socket.recv(numToRead - num)
            num = num + len(letti)
            lettiTot = lettiTot + letti

        return lettiTot #restituisco la stringa letta
    # end of sockread method


    def checkfile(self, filename):
        """
        this method verify the presence of file into file system through his path, specified as parameter in function call
        """
        try :
            f = open(filename)
        except Exception, expt :
            print "File does not exist -> %s" % expt + "\n"
        else:
            f.close()
    # end of checkfile method

    def addNeighbour(self, IP, port):
        newline = []
        newline.append(IP)
        newline.append(port)
        newline.append(time.time()) #numero di secondi dall'epoca (?)
        self.neighTable.append(newline) #inserisco la nuova riga nella tabella dei vicini
        print self.neighTable #TODO debug

    def replaceOLD(self, IP, port):
        self.new_neighbour = []
        oldest=self.neighTable[0[2]] #inizializzo la variabile "piu' vecchio alla prima entry della tabella
        for i in self.neighTable: # i e' un elemento di neighTable
            tmp=self.neighTable[i[2]]
            if tmp > oldest :
                oldest = tmp
                to_replace = i
        # ho individuato l'elemento che non uso da piu' tempo e lo rimpiazzo con un neighbour nuovo
        self.neighTable[to_replace[0]]= IP
        self.neighTable[to_replace[1]]= port
        self.neighTable[to_replace[2]]= time.time()
    #end of method clearOld


    def generate_pktID(self):
        size=16
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.choice(chars) for x in range(size))

    def openConn(self, IP, port):
        #mi connetto al vicino
        neigh_addr = (IP, port)
        try:
            print "mi connetto al vicino" #TODO debug
            neigh_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            neigh_socket.connect(neigh_addr)
        except IOError, expt: #IOError exception includes a sub-exception socket.error
            print "Error occured in Connection with neighbour -> %s" % expt + "\n"
        else:
            return neigh_socket


    def closeConn(self, socket):
        #mi disconnetto dal vicino
        try:
            socket.close()
        except IOError, expt: #IOError exception includes a sub-exception socket.error
            print "Error occured in Disconnection with neighbour -> %s" % expt + "\n"


    def findfile(self):

        print ""

    def findneigh(self):

        print "Find neighbours..."
        neigh_TTL = "0" #inizializzazione fittizia per il while di conttollo
        while int(neigh_TTL) < 1: #verifico che non venga inserito un valore non possibile
            neigh_TTL = raw_input("Insert neighbours TTL (min=1, typ=2): ")
        neigh_TTL_form = '%(#)02d' % {"#" : int(neigh_TTL)}
        pktID =  self.generate_pktID()
        print "pktID sent for query flooding: " + pktID
        for n in self.neighTable: #n e' un elemento di neighTable
            neigh_sock = self.openConn(self.neighTable[n[0]], self.neighTable[n[1]]) #passo ip e porta
            neigh_sock.send("NEAR" + pktID + self.my_IP_form + self.my_port_form + neigh_TTL_form)
            #TODO: verificare che vada bene, perchè posso ricevere anche piu' di una risposta
            ack=self.sockread(neigh_sock,20)
            if ack[:16] == "ANEA":
                print "OK, ack received" #TODO: debug
                if ack[16:20] == pktID: #controllo che il pktID sia lo stesso di quello che ho generato io per la richiesta
                    data = self.sockread(neigh_sock,20)
                    neigh_IP = data[:15]
                    neigh_port = data[15:20]
                    self.replaceOLD(neigh_IP,neigh_port)

                    #TODO implementare funzione per eventuale aggiunta neighbours alla neighTable
            else:
                print "Expecting 'ANEA': ack parsing failed"
                break
            self.closeConn(neigh_sock)






    def goout(self):
        gp.stop=True


    def error(self):
        print "Option not valid: try again!\n"
    # end of error method



    def doYourStuff(self):

        """
        This methods allow user to navigate into menu
        """

        print "Choose between the following options, typing the number:\n"

        print "1. Search file"
        print "2. Find neighbours"
        print "3. Exit program\n"

        choice = raw_input("Choose an option: ")

        opt = {

            '1' : self.findfile,
            '2' : self.findneigh,
            '3' : self.goout

        }

        print ""

        opt.get(choice,self.error)() #se l'utente ha digitato un qualcosa che non esiste, viene chiamata error()

    # end of doYourStuff method



if __name__ == "__main__":

    gp = GnutellaPeer() #inizializzazione


    while gp.stop==False:

        gp.doYourStuff() #stampa del menu ed esecuzione dell'operazione scelta