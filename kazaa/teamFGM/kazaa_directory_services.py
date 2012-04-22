__author__ = 'GuiducciGrillandaLoPiccolo'

import kazaa_peer_services #per neighTable

import socket # networking module
import threading
import os
import re
import time
import hashlib #per calcolare l'md5 dei file
import string
import random


class Service():

    """
    This class implements all the methods that will be inherited by others classes
    """

    pktTable = [] #e' la tabella contenente gli ID dei pacchetti gia' ricevuti in passato
    #tutte le classi che estendono Service possono accedervi ed e' come se fosse una tabella fatta sul db

    myQueryTable = [] #tabella in cui io salvo le mie ricerche (pktid,time)

    peersdb = [] #database con tutti i peer a me connessi (sessionID, IP, port)

    filesdb = [] #tabella in cui salvo i file che conosco (sessionID, filemd5, filename)

    matchTable = [] #tabella con la collezione di tutti gli AQUE ricevuti (pktID, ipp2p, pp2p, filemd5, filename)
    #la dovro' scorrere per andare poi a costruire la risposta alla FIND

    def getPktTable(self):
        return self.pktTable

    def setPktTable(self,pktTable):
        self.pktTable = pktTable

    def getMyQueryTable(self):
        return self.myQueryTable

    def setMyQueryTable(self,myQueryTable):
        self.myQueryTable = myQueryTable

    def getPeersdb(self):
        return self.peersdb

    def setPeersdb(self,peersdb):
        self.peersdb = peersdb

    def getFileTable(self):
        return self.fileTable

    def setFileTable(self,fileTable):
        self.fileTable = fileTable

    def getMatchTable(self):
        return self.matchTable

    def setMatchTable(self,matchTable):
        self.matchTable = matchTable

    def getFilesdb(self):
        return self.filesdb

    def setFilesdb(self,filesdb):
        self.filesdb = filesdb

    def addPeerTodb(self, sessionID, IP, port):

        #formatto IP
        IP_split = IP.split(".")
        IP_1 = '%(#)03d' % {"#" : int(IP_split[0])}
        IP_2 = '%(#)03d' % {"#" : int(IP_split[1])}
        IP_3 = '%(#)03d' % {"#" : int(IP_split[2])}
        IP_4 = '%(#)03d' % {"#" : int(IP_split[3])}
        IP_form = IP_1 + "." + IP_2 + "." + IP_3 + "." + IP_4 #IP formattato per bene

        #formatto porta
        port_form = '%(#)05d' % {"#" : int(port)} #porta formattata per bene

        newpeer = []
        newpeer.append(sessionID)
        newpeer.append(IP_form)
        newpeer.append(port_form)
        self.peersdb.append(newpeer)

        print self.peersdb

    def generate_pktID(self):
        size=16
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.choice(chars) for x in range(size))
        #end of method generate_pktID


    def sockread(self, socket, numToRead):
        """
        This method allow a trusted reading from socket, without loss any byte.
        The reading from socket persist until the entire number of byte given by parameter were read from socket.
        The socket object have to be given as a open socket connection.
        """
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
            #print "Connecting with neighbour " + IP #TODO debug
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
            print "Error occured in Disconnection from neighbour -> %s" % expt + "\n"
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

    def addFileTodb(self, sessionID, filemd5, filename):

        #devo aggiornare i filename dei file che hanno l'md5 del nuovo file
        #e infine inserire, se non c'e' gia', il nuovo file

        filesdb = self.getFilesdb() #(sessionID, filemd5, filename)

        #aggiorno
        for i in range(0,len(filesdb)):
            if filesdb[i][1] == filemd5: #se il campo md5 e' uguale
                filesdb[i][2] = filename #sovrascrivo il nome

        notFound = True

        for i in range(0,len(filesdb)):
            if filesdb[i][0] == sessionID and filesdb[i][1] == filemd5:
                notFound = False

        if notFound: #il file non era presente nella tabellina, lo aggiungo

            #inserisco
            new_file = []
            new_file.append(sessionID)
            new_file.append(filemd5)
            new_file.append(filename)
            filesdb.append(new_file)

        self.setFilesdb(filesdb)

        print self.getFilesdb()


    def delFileFromdb(self, sessID, filemd5):

        filesdb = self.getFilesdb() #(sessionID, filemd5, filename)

        #rimuovo
        i = 0
        while i < len(filesdb):
            if i >= len(filesdb):
                break
            if filesdb[i][0] == sessID and filesdb[i][1] == filemd5:
                filesdb.pop(i)
            else:
                i = i+1


        self.setFilesdb(filesdb)

        print self.getFilesdb()

    def delPeerFilesFromdb(self, sessID):

        cont = 0

        filesdb = self.getFilesdb() #(sessionID, filemd5, filename)

        #rimuovo tutti i files di quel peer
        i = 0
        while i < len(filesdb):
            if i >= len(filesdb):
                break
            if filesdb[i][0] == sessID: #se trovo la riga da cancellare non procedo col contatore
                filesdb.pop(i)
                cont = cont + 1
            else: #se la riga non va cancellata, procedo col contatore
                i = i+1


        self.setFilesdb(filesdb)

        print self.getFilesdb()

        return cont

    def delPeerFromdb(self,sessID):

        peersdb = self.getPeersdb()

        #rimuovo
        i = 0
        while i < len(peersdb):
            if i >= len(peersdb):
                break
            if peersdb[i][0] == sessID:
                peersdb.pop(i)
            else:
                i = i+1


        self.setPeersdb(peersdb)

        print self.getPeersdb()


    def addPktToTable(self, pktID): #scrivo sulla tabella che ho esaminato il pacchetto

        pktTable = self.getPktTable()

        newPkt = []
        newPkt.append(pktID)
        newPkt.append(time.time())
        pktTable.append(newPkt)
        self.setPktTable(pktTable)


    def cleanPktTable (self):
        """
        This method provides to clean pktTable, by deleting all packets that was added in  last 20 seconds
        after receiving pktID (or his creation)
        """
        #faccio la pulizia della tabella dei pacchetti
        #eliminando quelli piu' vecchi di 20 secondi
        now = time.time()

        pktTable = self.getPktTable()

        for i in range(0,len(pktTable)):

            if i>=len(pktTable):
                break

            if now - pktTable[i][1] > 20: #se sono passati piu' di 20 secondi elimino la riga dalla tabella

                pktTable.pop(i)

        self.setPktTable(pktTable)


    def checkPktAlreadySeen(self, pktID): #metodo per capire se il pacchetto e' passato sotto le mie mani negli ultimi 20 secondi

        pktTable = self.getPktTable()

        for i in range (0,len(pktTable)):

            if pktTable[i][0] == pktID: #se ho trovato il pacchetto
                return True

        #se sono uscita indenne dal ciclo (pacchetto non trovato)
        return False


    def checkPeerByIPPort(self,IP,port): #metodo per capire se il peer e' gia' loggato

        peersdb = self.getPeersdb()

        for i in range (0,len(peersdb)):

            if peersdb[i][1] == IP and int(peersdb[i][2]) == int(port): #se ho trovato il peer
                return True

        #se sono uscita indenne dal ciclo (peer non trovato)
        return False

    def checkPeerBySessID(self,sessID): #metodo per capire se il peer e' gia' loggato

        peersdb = self.getPeersdb()

        for i in range (0,len(peersdb)):

            if peersdb[i][0] == sessID: #se ho trovato il peer
                return True

        #se sono uscita indenne dal ciclo (peer non trovato)
        return False

    def getIPPortBySessID(self,sessID):

        peersdb = self.getPeersdb()

        for i in range (0,len(peersdb)):

            if peersdb[i][0] == sessID: #se ho trovato il peer
                info = []
                info.append(peersdb[i][1])
                info.append(peersdb[i][2])
                return info


    def generate_sessID(self):
        size=16
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.choice(chars) for x in range(size))
        #end of method generate_pktID


class Login(threading.Thread, Service): #AGGIORNATA -- DA CONTROLLARE

    def __init__(self, socketclient, addrclient, my_IP_form, my_port_form):

        threading.Thread.__init__(self)

        # info sul peer che si connette, magari servono
        self.socketclient = socketclient
        self.addrclient = addrclient
        self.my_IP_form = my_IP_form
        self.my_port_form = my_port_form


    def run(self):

        login = self.sockread(self.socketclient,20)
        print "received LOGI" + login + " from " + self.addrclient[0] + ":" + str(self.addrclient[1])
        ipp2p = login[:15]
        pp2p = login[15:20]

        #calcolo un session id ed eventuamente aggiungo il peer al mio dababase dei peer connessi

        if self.checkPeerByIPPort(ipp2p,pp2p): #peer gia' loggato
            print "peer gia' loggato, non lo aggiungo"
            self.socketclient.sendall("ALGI" + "0000000000000000")
            print "sent ALGI" + "0000000000000000" + " to " + self.addrclient[0] + ":" + str(self.addrclient[1])

        else:

            sessID = self.generate_sessID()
            self.addPeerTodb(sessID, ipp2p, pp2p)
            self.socketclient.sendall("ALGI" + sessID)
            print "sent ALGI" + sessID + " to " + self.addrclient[0] + ":" + str(self.addrclient[1])

        print ""

        # end of run method


class Logout(threading.Thread, Service): #AGGIORNATA -- DA CONTROLLARE

    def __init__(self, socketclient, addrclient, my_IP_form, my_port_form):

        threading.Thread.__init__(self)

        # info sul peer che si connette, magari servono
        self.socketclient = socketclient
        self.addrclient = addrclient
        self.my_IP_form = my_IP_form
        self.my_port_form = my_port_form


    def run(self):

        logout = self.sockread(self.socketclient,16)
        print "received LOGO" + logout + " from " + self.addrclient[0] + ":" + str(self.addrclient[1])
        sessID = logout[:16]

        if self.checkPeerBySessID(sessID):

            num_del = self.delPeerFilesFromdb(sessID)
            num_del_form = '%(#)03d' % {"#" : int(num_del)}

            #cancello il peer da peersdb
            self.delPeerFromdb(sessID)

            #invio l'ack a chi ha effettuato il login sulla socketclient
            self.socketclient.sendall("ALGO" + num_del_form)
            print "sent ALGO" + num_del_form + " to " + self.addrclient[0] + ":" + str(self.addrclient[1])

        else:

            print "il peer non era loggato"

            self.socketclient.sendall("ALGO" + "999")
            print "sent ALGO" + "999" + " to " + self.addrclient[0] + ":" + str(self.addrclient[1])

        print ""

        # end of run method


class AddFile(threading.Thread, Service): #AGGIORNATA -- DA CONTROLLARE

    def __init__(self, socketclient, addrclient, my_IP_form, my_port_form):

        threading.Thread.__init__(self)

        # info sul peer che si connette, magari servono
        self.socketclient = socketclient
        self.addrclient = addrclient
        self.my_IP_form = my_IP_form
        self.my_port_form = my_port_form


    def run(self):

        addfile = self.sockread(self.socketclient,132)
        print "received ADFF" + addfile + " from " + self.addrclient[0] + ":" + str(self.addrclient[1])
        sessID = addfile[:16]
        filemd5 = addfile[16:32]
        filename_form = addfile[32:132]
        filename = filename_form.strip(" ")

        self.addFileTodb(sessID, filemd5, filename) #funzione che si occupa dell'aggiunta file controllando tutto per benino

        print ""

        # end of run method

class DeleteFile(threading.Thread, Service): #AGGIORNATA -- DA CONTROLLARE

    def __init__(self, socketclient, addrclient, my_IP_form, my_port_form):

        threading.Thread.__init__(self)

        # info sul peer che si connette, magari servono
        self.socketclient = socketclient
        self.addrclient = addrclient
        self.my_IP_form = my_IP_form
        self.my_port_form = my_port_form


    def run(self):

        delfile = self.sockread(self.socketclient,32)
        print "received DEFF" + delfile + " from " + self.addrclient[0] + ":" + str(self.addrclient[1])
        sessID = delfile[:16]
        filemd5 = delfile[16:32]

        self.delFileFromdb(sessID, filemd5)

        print ""

        # end of run method


class FindFile(threading.Thread, Service): #DA SCRIVERE

    def __init__(self, socketclient, addrclient, my_IP_form, my_port_form):

        threading.Thread.__init__(self)

        # info sul peer che si connette, magari servono
        self.socketclient = socketclient
        self.addrclient = addrclient
        self.my_IP_form = my_IP_form
        self.my_port_form = my_port_form

    def searchFiles(self,search_string): #DA COMPLETARE!

        lista_files = []

        #ricerca sulla tabella filesdb di kazaa_directory_services
        filesdb = self.getFilesdb()

        lista_files = filesdb #ossia ritorno tutti i files che conosco (in realta' dovrei ritornare solo quelli che matchano)
        #sessionID, filemd5, filename

        return lista_files


    def run(self):

        findfile = self.sockread(self.socketclient,36)
        print "received FIND" + findfile + " from " + self.addrclient[0] + ":" + str(self.addrclient[1])
        sessID = findfile[:16]
        ricerca_form = findfile[16:36]
        ricerca = ricerca_form.strip(" ")

        pktID = self.generate_pktID()

        ttl = raw_input("Insert ttl: ")
        ttl_form = '%(#)02d' % {"#" : int(ttl)}

        #mando QUER a tutti i miei amici
        neighService = kazaa_peer_services.Service()
        neighTable = neighService.getNeighTable()

        for n in range(0,len(neighTable)): #n e' l'indice del vicino

            neigh_sock = self.openConn(neighTable[n][0], neighTable[n][1]) #passo ip e porta
            neigh_sock.sendall("QUER" + pktID + self.my_IP_form + self.my_IP_form + ttl_form + ricerca_form)
            print "sent QUER" + pktID + self.my_IP_form + str(self.my_IP_form) + ttl_form + ricerca_form + " to " + neighTable[n][0] + ":" + str(neighTable[n][1])
            self.closeConn(neigh_sock)

        #cerco anche all'interno dei miei files
        files = self.searchFiles(ricerca) #files = lista di files che matchano la ricerca
                                            #sessionID, filemd5, filename

        if(len(files)==0):
            print "No file matches with query's search" #TODO debug


        else: #ho trovato almeno un file che matchi la ricerca
            print "Found #" + str(len(files)) + " files that meet query's search" #TODO debug

            #aggiorno la mia tabella matchTable
            for f in range(0,len(files)): #f = indice riga (una riga=un file)

                IPPort = self.getIPPortBySessID(files[f][0]) #dal sessionID ricavo array con IP e porta
                ipp2p = IPPort[0]
                pp2p = IPPort[1]

                filemd5 = files[f][1]
                filename = files[f][2]

                matchTable = self.getMatchTable()

                new_match = []
                new_match.append(pktID)
                new_match.append(ipp2p)
                new_match.append(pp2p)
                new_match.append(filemd5)
                new_match.append(filename)

                matchTable.append(new_match)

                self.setMatchTable(matchTable)

        print self.getMatchTable()

        time.sleep(20) #non e' esattamente come dovrebbe essere, TODO sistemare

        #faccio una prova di esempio
        tosend = "AFIN0010000000000000000                                                                                               pippo001999.999.999.99911111"
        #in realta' dovrei calcolare quanti md5 differenti ci sono e formattare per bene il pacchetto da inviare
        #idmd5[3B].{Filemd5_i[16B].Filename_i[100B].#copy_i[3B].{IPP2P_i_j[15B].PP2P_i_j[5B]}(j=1..#copy_i)}(i=1..#idmd5)

        self.socketclient.sendall(tosend)

        print ""

        # end of run method