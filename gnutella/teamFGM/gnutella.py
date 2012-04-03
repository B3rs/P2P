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
        self.n1_IP = "0.0.0.0"
        self.n1_port = 9999
        self.n2_IP = "0.0.0.0"
        self.n2_port = 9999

        #tabella vicini
        prova = gnutella_service.Service()
        print "aggiungo vicino n.1"
        prova.addNeighbour(self.n1_IP,self.n1_port)
        print prova.getNeighTable()
        print "aggiungo vicino n.2"
        prova.addNeighbour(self.n2_IP,self.n2_port)
        print prova.getNeighTable()

    # end of __init__ method

# Definition of auxiliary methods


    def generate_pktID(self):
        size=16
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.choice(chars) for x in range(size))
    #end of method generate_pktID

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
    # end of method openConn


    def closeConn(self, socket):
        #mi disconnetto dal vicino
        try:
            socket.close()
        except IOError, expt: #IOError exception includes a sub-exception socket.error
            print "Error occured in Disconnection with neighbour -> %s" % expt + "\n"
    # end of method closeConn


    def findFile(self):

        print "Find files...\n"

        query_TTL = "0" #inizializzazione fittizia per il while di controllo stdin
        search = raw_input("Insert a search string: ")
        print search
        search_form = '%(#)020s' % {"#" : search} #formatto la stringa di ricerca
        while int(query_TTL) < 1 :
            query_TTL = raw_input("Insert TTL for query request (min=1, typ=4 or 5): ")
        query_TTL_form = '%(#)02d' % {"#" : int(query_TTL)}
        pktID = self.generate_pktID()
        print "pktID generated for query flooding files: " + pktID
        # invio la richiesta di query flooding a tutti i miei vicini
        prova = gnutella_service.Service()
        neighTable = prova.getNeighTable()
        for n in range(0,len(neighTable)):
            #neigh_sock = self.openConn(neighTable[n][0], neighTable[n][1]) #passo ip e porta
            #neigh_sock.sendall("QUER" + pktID + self.my_IP_form + self.my_port_form + query_TTL_form + search_form)
            print "QUER" + str(pktID) + self.my_IP_form + str(self.my_port_form) + query_TTL_form + search_form
            #self.closeConn(neigh_sock)

    # end of findFile method


    def findNeigh(self):

        print "Find neighbours..."

        neigh_TTL = "0" #inizializzazione fittizia per il while di conttollo stdin
        while int(neigh_TTL) < 1: #verifico che non venga inserito un valore non possibile
            neigh_TTL = raw_input("Insert neighbours TTL (min=1, typ=2): ")
        neigh_TTL_form = '%(#)02d' % {"#" : int(neigh_TTL)}
        pktID =  self.generate_pktID()
        print "pktID generated for query flooding neighbours: " + pktID
        # invio la richiesta di query flooding a tutti i miei vicini
        prova = gnutella_service.Service()
        neighTable = prova.getNeighTable()
        for n in range(0,len(neighTable)):
            #neigh_sock = self.openConn(neighTable[n][0], neighTable[n][1]) #passo ip e porta
            #neigh_sock.sendall("NEAR" + pktID + self.my_IP_form + self.my_port_form + neigh_TTL_form)
            print "NEAR" + str(pktID) + self.my_IP_form + str(self.my_port_form) + neigh_TTL_form
            #self.closeConn(neigh_sock)

    # end of findNeigh method


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

        print "1. Search file"
        print "2. Find neighbours"
        print "3. Exit program\n"

        choice = raw_input("Choose an option: ")

        opt = {

            '1' : self.findFile,
            '2' : self.findNeigh,
            '3' : self.goOut

        }

        print ""

        opt.get(choice,self.error)() #se l'utente ha digitato un qualcosa che non esiste, viene chiamata error()

    # end of doYourStuff method



if __name__ == "__main__":

    gp = GnutellaPeer() #inizializzazione

    while not gp.stop:

        gp.doYourStuff() #stampa del menu ed esecuzione dell'operazione scelta