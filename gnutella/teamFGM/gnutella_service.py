__author__ = 'Frencina'

import socket # networking module
import threading
import os
import re

class Query(threading.Thread):

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

    def searchFiles(self,search_string):

        lista_files = []

        dir = "/Users/Frencina/PycharmProjects/P2P/gnutella/teamFGM" #TODO setup your own directory
        dirEntries = os.listdir(dir)
        for entry in dirEntries:
            if re.match(".*search_string.*", entry):
                print entry
                lista_files.append()
        print lista_files
        return lista_files

    def run(self):

        #quando mi arriva una query devo fare due cose:
        #rispondere con un aque nel caso io abbia il file
        #e diffondere pacchetto se TTL>1 e decrementarlo

        query = self.sockread(self.socketclient,58)
        pktid = query[:16]
        print pktid
        ipp2p = query[16:31]
        print ipp2p
        pp2p = query[31:36]
        print pp2p
        ttl = query[36:38]
        print ttl
        ricerca = query[38:58]
        print ricerca

        lista = self.searchFiles(ricerca)

        #mando un aque per ogni file trovato

        #aggiorno la mia tabella dei pacchetti ricevuti

        #devo diffondere il pacchetto ai miei vicini dopo aver decrementato il TTL


    # end of run method

class AckQuery(threading.Thread):

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

        #codice
        print ""
    # end of run method

class Near(threading.Thread):

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

        #codice
        print ""

    # end of run method

class AckNear(threading.Thread):

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

        #codice
        print ""

    # end of run method

class Download(threading.Thread):

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

        #codice
        print ""

    # end of run method