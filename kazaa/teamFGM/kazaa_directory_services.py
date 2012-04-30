__author__ = 'GuiducciGrillandaLoPiccolo'

import kazaa_peer_services

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

    peersdb = [] #database con tutti i peer a me connessi (sessionID, IP, port)

    filesdb = [] #tabella in cui salvo i file che conosco (sessionID, filemd5, filename)

    matchTable = [] #tabella con la collezione di tutti gli AQUE ricevuti (pktID, ipp2p, pp2p, filemd5, filename)
    #la dovro' scorrere per andare poi a costruire la risposta alla FIND

    p2pPort = [""] #porta per il p2p (es.09999)

    def getP2pPort(self):
        return self.p2pPort[0]

    def setP2pPort(self,p2pPort):
        self.p2pPort[0] = p2pPort

    def getPeersdb(self):
        return self.peersdb

    def setPeersdb(self,peersdb):
        self.peersdb = peersdb

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
            #print "Connecting with neighbour " + IP
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

        return cont #ritorno il numero di file rimossi

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
                return info #ritorno un array in cui il primo elemento e' l'ip, il secondo la porta


    def generate_sessID(self):
        size=16
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.choice(chars) for x in range(size))
        #end of method generate_pktID


class Login(threading.Thread, Service):

    def __init__(self, socketclient, addrclient, my_IP_form, dir_port_form):

        threading.Thread.__init__(self)

        # info sul peer che si connette, magari servono
        self.socketclient = socketclient
        self.addrclient = addrclient
        self.my_IP_form = my_IP_form
        self.dir_port_form = dir_port_form


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

        else: #peer non ancora loggato, lo aggiungo

            sessID = self.generate_sessID()
            self.addPeerTodb(sessID, ipp2p, pp2p)
            self.socketclient.sendall("ALGI" + sessID)
            print "sent ALGI" + sessID + " to " + self.addrclient[0] + ":" + str(self.addrclient[1])

        print ""

        # end of run method


class Logout(threading.Thread, Service):

    def __init__(self, socketclient, addrclient, my_IP_form, dir_port_form):

        threading.Thread.__init__(self)

        # info sul peer che si connette, magari servono
        self.socketclient = socketclient
        self.addrclient = addrclient
        self.my_IP_form = my_IP_form
        self.dir_port_form = dir_port_form


    def run(self):

        logout = self.sockread(self.socketclient,16)
        print "received LOGO" + logout + " from " + self.addrclient[0] + ":" + str(self.addrclient[1])
        sessID = logout[:16]

        if self.checkPeerBySessID(sessID): #se il peer era loggato

            num_del = self.delPeerFilesFromdb(sessID) #cancello i files che aveva aggiunto e ritorno il numero di files
            num_del_form = '%(#)03d' % {"#" : int(num_del)}

            #cancello il peer da peersdb
            self.delPeerFromdb(sessID) #cancello il peer dalla tabella peersdb

            #invio l'ack
            self.socketclient.sendall("ALGO" + num_del_form)
            print "sent ALGO" + num_del_form + " to " + self.addrclient[0] + ":" + str(self.addrclient[1])

        else: #se il peer non era loggato

            print "il peer non era loggato"

            self.socketclient.sendall("ALGO" + "999") #gli mando un numero fittizio
            print "sent ALGO" + "999" + " to " + self.addrclient[0] + ":" + str(self.addrclient[1])

        print ""

        # end of run method


class AddFile(threading.Thread, Service):

    def __init__(self, socketclient, addrclient, my_IP_form, dir_port_form):

        threading.Thread.__init__(self)

        # info sul peer che si connette, magari servono
        self.socketclient = socketclient
        self.addrclient = addrclient
        self.my_IP_form = my_IP_form
        self.dir_port_form = dir_port_form


    def run(self):

        addfile = self.sockread(self.socketclient,132)
        print "received ADFF" + addfile + " from " + self.addrclient[0] + ":" + str(self.addrclient[1])
        sessID = addfile[:16]
        filemd5 = addfile[16:32]
        filename_form = addfile[32:132]
        filename = filename_form.strip(" ")

        self.addFileTodb(sessID, filemd5, filename) #aggiunta del file (fa lei tutti i controlli)

        print ""

        # end of run method

class DeleteFile(threading.Thread, Service):

    def __init__(self, socketclient, addrclient, my_IP_form, dir_port_form):

        threading.Thread.__init__(self)

        # info sul peer che si connette, magari servono
        self.socketclient = socketclient
        self.addrclient = addrclient
        self.my_IP_form = my_IP_form
        self.dir_port_form = dir_port_form


    def run(self):

        delfile = self.sockread(self.socketclient,32)
        print "received DEFF" + delfile + " from " + self.addrclient[0] + ":" + str(self.addrclient[1])
        sessID = delfile[:16]
        filemd5 = delfile[16:32]

        self.delFileFromdb(sessID, filemd5) #cancellazione del file (fa lei tutti i controlli)

        print ""

        # end of run method


class FindFile(threading.Thread, Service):

    def __init__(self, socketclient, addrclient, my_IP_form, dir_port_form):

        threading.Thread.__init__(self)

        # info sul peer che si connette, magari servono
        self.socketclient = socketclient
        self.addrclient = addrclient
        self.my_IP_form = my_IP_form
        self.dir_port_form = dir_port_form


    def searchFiles(self,search_string): #ATTENZIONE! deve essere la stessa che c'e' in kazaa_peer_services)

        lista_files = []

        #ricerca nella tabella filesdb
        filesdb = self.getFilesdb()

        for i in range(0,len(filesdb)):
            if filesdb[i][2].lower().find(search_string.lower()) != -1: #filesdb[i][2] e' il nome del file i-esimo
                new_file = []
                new_file.append(filesdb[i][0]) #sessionID
                new_file.append(filesdb[i][1]) #filemd5
                new_file.append(filesdb[i][2]) #filename
                lista_files.append(new_file)

        return lista_files #lista con i files che matchano la ricerca


    def run(self):

        findfile = self.sockread(self.socketclient,36)
        print "received FIND" + findfile + " from " + self.addrclient[0] + ":" + str(self.addrclient[1])
        sessID = findfile[:16] #sessionID del peer che ha effettuato la ricerca
        ricerca_form = findfile[16:36]
        ricerca = ricerca_form.strip(" ")

        #da quando ricevo questo pacchetto ho 20 secondi di tempo per ricevere le risposte dai vari superpeer
        start = time.time()

        ttl = 2 #ttl statico
        ttl_form = '%(#)02d' % {"#" : int(ttl)}

        pktID = self.generate_pktID() #genero pktID

        #aggiungo il pktID a quelli della myQueryTable cosi' quando mi tornano i pacchetti AQUE di risposta
        #riesco a capire se devo scartarli o meno in base a quanti secondi sono passati
        queryService = kazaa_peer_services.Service()
        myQueryTable = queryService.getMyQueryTable()
        new_entry = []
        new_entry.append(pktID)
        new_entry.append(time.time())
        myQueryTable.append(new_entry)
        queryService.setMyQueryTable(myQueryTable)

        #mando QUER a tutti i miei amici
        neighService = kazaa_peer_services.Service()
        neighTable = neighService.getNeighTable()

        for n in range(0,len(neighTable)): #n e' l'indice del vicino

            neigh_sock = self.openConn(neighTable[n][0], neighTable[n][1]) #passo ip e porta
            neigh_sock.sendall("QUER" + pktID + self.my_IP_form + self.getP2pPort() + ttl_form + ricerca_form)
            print "sent QUER" + pktID + self.my_IP_form + str(self.getP2pPort()) + ttl_form + ricerca_form + " to " + neighTable[n][0] + ":" + str(neighTable[n][1])
            self.closeConn(neigh_sock)

        #cerco anche all'interno dei miei files
        files = self.searchFiles(ricerca) #files = lista di files che matchano la ricerca
                                            #sessionID, filemd5, filename

        if(len(files)==0):
            print "No file matches with query's search in my superpeer"


        else: #ho trovato almeno un file che matchi la ricerca
            print "Found #" + str(len(files)) + " files that meet query's search in my superpeer"

            #aggiorno la mia tabella matchTable
            for f in range(0,len(files)): #f = indice riga (una riga=un file)

                IPPort = self.getIPPortBySessID(files[f][0]) #dal sessionID ricavo array con IP e porta del peer che ha il file
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

                self.setMatchTable(matchTable) #aggiorno matchTable

        while True:
            if time.time() - start > 20: #se da quando ho iniziato finora sono passati piu' di 20 secondi posso proseguire
                break
            time.sleep(1)

        #ora devo mandare la mega risposta al peer che ha effettuato la ricerca (che e' ancora la' che aspetta)

        matchTable = self.getMatchTable() #pktID, ipp2p, pp2p, filemd5, filename
        #puo' essere che piu' file con lo stesso md5 abbiano nome di file differente,
        #in quanto provenienti da differenti supernodi, si utilizza un solo nome tra quelli possibili,
        #lasciando tale scelta  libera nella implementazione.

        print matchTable

        #formattazione pacchetto finale:
        #AFIN.idmd5[3B].{Filemd5_i[16B].Filename_i[100B].#copy_i[3B].{IPP2P_i_j[15B].PP2P_i_j[5B]}(j=1..#copy_i)}(i=1..#idmd5)

        i = 0
        num_md5 = 0 #numero dei differenti idmd5
        partial = ""

        while i < len(matchTable):
            if i >= len(matchTable):
                break
            if matchTable[i][0] == pktID:
                #ho trovato una riga con un nuovo md5
                num_md5 = num_md5 + 1 #incremento num dei diversi md5
                cur_filemd5 = matchTable[i][3]
                cur_filename = matchTable[i][4]
                cur_filename_form = '%(#)0100s' % {"#" : cur_filename}
                num_copy = 1
                cur_ip = matchTable[i][1]
                cur_port = matchTable[i][2]
                ip_porta = cur_ip + cur_port

                j=0

                while j < len(matchTable): #scorro la tabella alla ricerca di altri md5 uguali
                    if j >= len(matchTable):
                        break
                    if matchTable[j][0] == pktID and i!=j and matchTable[i][3] == matchTable[j][3]: #se i due md5 sono uguali
                        num_copy = num_copy + 1
                        cur_ip = matchTable[j][1]
                        cur_port = matchTable[j][2]
                        ip_porta += cur_ip + cur_port #aggiungo ip e porta della copia corrente
                        matchTable.pop(j) #elimino la riga
                    else:
                        j = j+1

                #formatto il numero delle copie
                num_copy_form = '%(#)03d' % {"#" : int(num_copy)}

                #costruisco la stringa per questo particolare md5
                partial += cur_filemd5 + cur_filename_form + num_copy_form + ip_porta

                matchTable.pop(i)
            else:
                i = i+1

        #formatto il numero di differenti md5
        num_md5_form = '%(#)03d' % {"#" : int(num_md5)}

        #costruisco la stringa finale complessiva
        total = "AFIN" + num_md5_form + partial

        self.setMatchTable(matchTable)

        self.socketclient.sendall(total) #invio mega pacchetto al peer che aveva effettuato la ricerca
        print "sent " + total + " to " + self.addrclient[0] + ":" + str(self.addrclient[1])

        print ""

        # end of run method