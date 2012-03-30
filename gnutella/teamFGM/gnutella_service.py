__author__ = 'Frencina'

import socket # networking module
import threading
import os
import re

#TODO risolvere problema: ogni classe ha la sua tabellina privata di pacchetti e vicini
#cosi' fa schifo perche' non si aggiornano le une con le altre
#bisogna fare una tabella unica e andarsi a leggere quella ogni volta con un getPtk() o getNeigh()
#potremmo per esempio mettere la tabella nella classe Service (parlarne insieme)

class Service():

    """
    In questa classe vanno messi tutti i metodi comuni ai vari servizi
    """

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

    def addPktToTable(self, pktID, pktTable): #scrivo sulla tabella che ho esaminato il pacchetto

        newPkt = []
        newPkt.append(pktID)
        newPkt.append(time.time())
        pktTable.append(newPkt)


    def cleanPktTable (self, pktTable):

        #faccio la pulizia della tabella dei pacchetti
        #eliminando quelli piu' vecchi di 300 secondi

        now = time.time()

        for i in range(0,len(pktTable)):

            if now - pktTable[i][1] > 300: #se sono passati piu' di 300 secondi elimino la riga dalla tabella

                pktTable.remove(i) #TODO controllare che la cancellazione di una riga si faccia cosi'


    def checkPktAlreadySeen(self, pktID, pktTable): #metodo per capire se il pacchetto e' passato sotto le mie mani negli ultimi 300 secondi

        for i in range (0,len(pktTable)):

            if pktTable[i][0] == pktID: #se ho trovato il pacchetto
                return True

        #se sono uscita indenne dal ciclo
        return False


class Query(threading.Thread, Service): #ereditarieta' multipla

    def __init__(self, socketclient, addrclient, neighTable, pktTable, my_IP, my_IP_form, my_port, my_port_form):

        threading.Thread.__init__(self)

        # info sul peer che si connette, magari servono
        self.socketclient = socketclient
        self.addrclient = addrclient
        self.neighTable = neighTable
        self.pktTable = pktTable
        self.my_IP = my_IP
        self.my_IP_form = my_IP_form
        self.my_port = my_port
        self.my_port_form = my_port_form


    def searchFiles(self,search_string):

        lista_files = []

        dir = "/Users/Frencina/PycharmProjects/P2P/gnutella/teamFGM" #TODO setup your own directory
        dirEntries = os.listdir(dir)
        for entry in dirEntries:
            if re.match(".*search_string.*", entry):
                print entry
                lista_files.append()
        return lista_files

    def run(self):

        query = self.sockread(self.socketclient,58)
        pktID = query[:16]
        print pktID
        ipp2p = query[16:31]
        print ipp2p
        pp2p = query[31:36]
        print pp2p
        ttl = query[36:38]
        print ttl
        ricerca = query[38:58]
        print ricerca
        ricerca = ricerca.strip(" ") #pulisco la stringa dagli spazi
        print ricerca

        self.cleanPktTable(self.pktTable) #pulizia della tabella dei pacchetti

        if self.checkPktAlreadySeen(): #se ho gia' ricevuto questo pacchetto
            print "pacchetto gia' ricevuto in passato. non faccio nulla"

        else:
            print "pacchetto nuovo. procedo."
            self.addPktToTable(pktID,self.pktTable) #aggiungo pacchetto alla tabella

            #procedo con tutto il resto

            #se il ttl e' maggiore di 1 devo ripropagare il pacchetto dopo aver decrementato il ttl
            #se tra i miei vicini c'e' anche chi ha effettuato la ricerca non devo mandarlo a lui
            if int(ttl)>1:

                #decremento il ttl prima di propagare il pacchetto
                ttl_decr = int(ttl) - 1
                ttl_form = '%(#)02d' % {"#" : int(ttl_decr)} #porta formattata per bene

                for n in range(0,len(self.neighTable)): #n e' l'indice del vicino

                    if self.neighTable[n][0] != ipp2p and self.neighTable[n][1] != int(pp2p):

                        neigh_sock = self.openConn(self.neighTable[n][0], self.neighTable[n][1]) #passo ip e porta
                        neigh_sock.sendall("QUER" + pktID + ipp2p + pp2p + ttl_form + ricerca)
                        print "QUER" + pktID + ipp2p + pp2p + ttl_form + ricerca
                        self.closeConn(neigh_sock)

            #in ogni caso cerco tra i miei files se ne ho uno che matcha la ricerca
            files = self.searchFiles(ricerca) #files = lista di files che matchano la ricerca

            if(len(files)==0):
                print "Non ho trovato nessun file che matchi la ricerca"

            else: #ho trovato almeno un file che matchi la ricerca
                print "Ho trovato " + len(files) + "che matchano la ricerca"
                print files

                #mando un aque a chi ha mandato la query per ogni file trovato
                for f in range(0,len(files)): #f = indice file

                    #files[f] dovrebbe essere il nome del file
                    filename = files[f]
                    print filename
                    filename_form = '%(#)0100s' % {"#" : filename} #formatto il nome del file
                    print filename_form

                    #calcolo l'md5 del file
                    filemd5 = self.md5_for_file(filename)

                    #invio l'ack a chi ha effettuato la ricerca
                    neigh_sock = self.openConn(ipp2p, int(pp2p)) #passo ip e porta
                    neigh_sock.sendall("AQUE" + pktID + self.my_IP_form + self.my_port_form + filemd5 + filename_form)
                    print "AQUE" + pktID + self.my_IP_form + self.my_port_form + filemd5 + filename_form
                    self.closeConn(neigh_sock)


    # end of run method

class AckQuery(threading.Thread, Service):

    def __init__(self, socketclient, addrclient, neighTable, pktTable):

        threading.Thread.__init__(self)

        # info sul peer che si connette, magari servono
        self.socketclient = socketclient
        self.addrclient = addrclient
        self.neighTable = neighTable
        self.pktTable = pktTable

    def run(self):

        #codice
        print ""
    # end of run method

class Near(threading.Thread, Service):

    def __init__(self, socketclient, addrclient, neighTable, pktTable):

        threading.Thread.__init__(self)

        # info sul peer che si connette, magari servono
        self.socketclient = socketclient
        self.addrclient = addrclient
        self.neighTable = neighTable
        self.pktTable = pktTable


    def run(self):

        #codice
        print ""

    # end of run method

class AckNear(threading.Thread, Service):

    def __init__(self, socketclient, addrclient, neighTable, pktTable):

        threading.Thread.__init__(self)

        # info sul peer che si connette, magari servono
        self.socketclient = socketclient
        self.addrclient = addrclient
        self.neighTable = neighTable
        self.pktTable = pktTable


    def run(self):

        #codice
        print ""

    # end of run method

class Download(threading.Thread, Service):

    def __init__(self, socketclient, addrclient, neighTable, pktTable):

        threading.Thread.__init__(self)

        # info sul peer che si connette, magari servono
        self.socketclient = socketclient
        self.addrclient = addrclient
        self.neighTable = neighTable
        self.pktTable = pktTable

    def run(self):

        #codice
        print ""

    # end of run method