__author__ = 'GuiducciGrillandaLoPiccolo'

import bittorrent_files

import socket # networking module
import threading
import string
import random


class Service():

    """
    This class implements all the methods that will be inherited by others classes
    """

    peersdb = [] #database con tutti i peer a me connessi (sessionID, IP, port)

    filesdb = [] #tabella in cui salvo i file che conosco (randomID, sessionID, filename, lenFile, lenPart, numPart, filetable)

    def getPeersdb(self):
        return self.peersdb

    def setPeersdb(self,peersdb):
        self.peersdb = peersdb

    def getFilesdb(self):
        return self.filesdb

    def setFilesdb(self,filesdb):
        self.filesdb = filesdb

    def printPeersdb(self):
        print ""
        print "_" * 200
        print '\033[95m' + "Peersdb" + '\033[0m'
        for i in range(0,len(self.peersdb)):
            print self.peersdb[i]
        print "_" * 200
        print ""

    def printFilesdb(self):
        print ""
        print "_" * 200
        print '\033[94m' + "Filesdb" + '\033[0m'
        print '\033[92m' + "randomID            sessionID           nomefile    lenfile[B]  lenpart[B]  numpart     sessionID            partlist" + '\033[0m'
        for i in range(0,len(self.filesdb)):
            print self.filesdb[i][0] + "\t" + self.filesdb[i][1] + "\t" + self.filesdb[i][2] + "\t" + self.filesdb[i][3] + "\t" + self.filesdb[i][4] + "\t\t" + self.filesdb[i][5]
            for j in range(0,len(self.filesdb[i][6])):
                print "\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t" + str(self.filesdb[i][6][j])
        print "_" * 200
        print ""

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

        self.printPeersdb()

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

            #recupero il file che aveva aggiunto il peer
            #provo a cancellare le parti aggiunte dal peer sorgente

            filesdb = self.getFilesdb() #recupero il database con tutti i file

            #vado a vedere se il peer e' una sorgente
            found = False
            for i in range(0,len(filesdb)):
                if filesdb[i][1] == sessID:
                    index_to_update = i
                    filetable_to_update = filesdb[i][6]
                    found = True

            can_logout = True
            num_parts = 0

            if found == True: #se il peer e' sorgente di un file

                fh = bittorrent_files.FileHandler() #inizializzazione di un filehandler

                logout = fh.tryLogout(filetable_to_update) #mi faccio restituire il [possologout?, numparti]

                can_logout = logout[0]
                num_parts = logout[1]

                if can_logout == False:
                    #rispondo al peer che non posso sloggarmi e non faccio nient'altro
                    num_parts_form = '%(#)010d' % {"#" : num_parts} #num_parts formattato per bene
                    self.socketclient.sendall("NLOG" + num_parts_form)
                    print "sent NLOG" + num_parts_form + " to " + self.addrclient[0] + ":" + str(self.addrclient[1])

                else:
                    #aggiorno la tabella alla luce della cancellazione
                    filesdb[index_to_update][6] = fh.getFileTable()
                    self.setFilesdb(filesdb)

            if can_logout: #cioe' sono una sorgente e mi posso sloggare oppure se sono un peer che non ha uploadato file

                filesdb = self.getFilesdb()
                for i in range(0,len(filesdb)): #per ogni file della tabella
                    fh = bittorrent_files.FileHandler() #inizializzazione di un filehandler
                    delete = fh.deleteParts(sessID, filesdb[i][6])
                    do_delete = delete[0]
                    if do_delete: #vuol dire che ho fatto una cancellazione nella filetable, devo aggiornare la tabella
                        filesdb[i][6] = fh.getFileTable()
                        self.setFilesdb(filesdb)
                        num_parts += delete[1]

                #cancello il peer da peersdb
                self.delPeerFromdb(sessID) #cancello il peer dalla tabella peersdb

                #rispondo al peer
                num_parts_form = '%(#)010d' % {"#" : num_parts} #num_parts formattato per bene
                self.socketclient.sendall("ALOG" + num_parts_form)
                print "sent ALOG" + num_parts_form + " to " + self.addrclient[0] + ":" + str(self.addrclient[1])


        else: #se il peer non era loggato

            print "il peer non era loggato"

            self.socketclient.sendall("ALOG" + "9999999999") #gli mando un numero fittizio
            print "sent ALOG" + "9999999999" + " to " + self.addrclient[0] + ":" + str(self.addrclient[1])

        self.printPeersdb()
        self.printFilesdb()

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

        addfile = self.sockread(self.socketclient,148)
        print "received ADDR" + addfile + " from " + self.addrclient[0] + ":" + str(self.addrclient[1])
        sessionID = addfile[:16]
        randomID = addfile[16:32]
        lenFile = addfile[32:42]
        lenPart = addfile[42:48]
        filename_form = addfile[48:148]
        filename = filename_form.strip(" ")

        fh = bittorrent_files.FileHandler() #inizializzazione di un filehandler

        numParts = fh.newTable(sessionID,int(lenFile),int(lenPart)) #mi faccio restituire il numPart

        filesdb = self.getFilesdb() #recupero il database con tutti i file

        newrow = []
        newrow.append(randomID)
        newrow.append(sessionID)
        newrow.append(filename)
        newrow.append(lenFile)
        newrow.append(lenPart)
        numParts_form = '%(#)08d' % {"#" : numParts} #numParts formattato per bene
        newrow.append(numParts_form)
        newrow.append(fh.getFileTable())

        filesdb.append(newrow)

        self.setFilesdb(filesdb)

        self.socketclient.sendall("AADR" + numParts_form)
        print "sent AADR" + numParts_form + " to " + self.addrclient[0] + ":" + str(self.addrclient[1])

        self.printFilesdb()

        print ""

        # end of run method


class LookFile(threading.Thread, Service):

    def __init__(self, socketclient, addrclient, my_IP_form, dir_port_form):

        threading.Thread.__init__(self)

        # info sul peer che si connette, magari servono
        self.socketclient = socketclient
        self.addrclient = addrclient
        self.my_IP_form = my_IP_form
        self.dir_port_form = dir_port_form


    def run(self):

        search = self.sockread(self.socketclient,36)
        print "received LOOK" + search + " from " + self.addrclient[0] + ":" + str(self.addrclient[1])
        sessionID = search[:16]
        ricerca_form = search[16:36]
        ricerca = ricerca_form.strip(" ")

        filesdb = self.getFilesdb() #recupero il database con tutti i file
        numrandomID = 0 #numero file che matchano la ricerca
        to_send = ""

        for i in range(0,len(filesdb)):
            if filesdb[i][2].lower().find(ricerca.lower()) != -1: #filesdb = randomID, sessionID, filename, lenFile, lenPart, numPart, filetable
                numrandomID += 1
                randomID = filesdb[i][0]
                filename = filesdb[i][2]
                lenfile = filesdb[i][3]
                lenpart = filesdb[i][4]
                filename_form = '%(#)0100s' % {"#" : filename} #filename formattato per bene
                to_send += randomID + filename_form + lenfile + lenpart

        numrandomID_form = '%(#)03d' % {"#" : numrandomID} #numrandomID formattato per bene

        total = numrandomID_form + to_send

        #rispondo al peer
        self.socketclient.sendall("ALOO" + total)
        print "sent ALOO" + total + " to " + self.addrclient[0] + ":" + str(self.addrclient[1])


class FetchFile(threading.Thread, Service):

    def __init__(self, socketclient, addrclient, my_IP_form, dir_port_form):

        threading.Thread.__init__(self)

        # info sul peer che si connette, magari servono
        self.socketclient = socketclient
        self.addrclient = addrclient
        self.my_IP_form = my_IP_form
        self.dir_port_form = dir_port_form

    def run(self):

        fetch = self.sockread(self.socketclient,32)
        print "received FCHU" + fetch + " from " + self.addrclient[0] + ":" + str(self.addrclient[1])
        sessionID = fetch[:16]
        randomID = fetch[16:32]

        filesdb = self.getFilesdb()

        for i in range(0,len(filesdb)):
            if filesdb[i][0] == randomID: #filesdb = randomID, sessionID, filename, lenFile, lenPart, numPart, filetable
                filetable = filesdb[i][6] #mi salvo la filetable che devo consultare

        fh = bittorrent_files.FileHandler() #inizializzazione di un filehandler

        total = fh.fetchstring(randomID,filetable,self.getPeersdb()) #mi faccio restituire la stringa lunga pronta per essere inviata

        #rispondo al peer
        self.socketclient.sendall("AFCH" + total)
        print "sent AFCH" + total + " to " + self.addrclient[0] + ":" + str(self.addrclient[1])

        # end of run method

class PostDownload(threading.Thread, Service):

    def __init__(self, socketclient, addrclient, my_IP_form, dir_port_form):

        threading.Thread.__init__(self)

        # info sul peer che si connette, magari servono
        self.socketclient = socketclient
        self.addrclient = addrclient
        self.my_IP_form = my_IP_form
        self.dir_port_form = dir_port_form


    def run(self):

        postdown = self.sockread(self.socketclient,40)
        print "received RPAD" + postdown + " from " + self.addrclient[0] + ":" + str(self.addrclient[1])
        sessionID = postdown[:16]
        randomID = postdown[16:32]
        numpart_to_update = postdown[32:40]

        filesdb = self.getFilesdb() #recupero il database con tutti i file

        #vado a cercare la riga con il file che mi interessa(randomID)
        for i in range(0,len(filesdb)):
            if filesdb[i][0] == randomID:
                index_to_update = i
                filetable_to_update = filesdb[i][6]

        fh = bittorrent_files.FileHandler() #inizializzazione di un filehandler

        numPeerPart = fh.updateTable(sessionID, int(numpart_to_update), filetable_to_update) #mi faccio restituire il numPeerPart

        numPeerParts_form = '%(#)08d' % {"#" : numPeerPart} #numPeerParts formattato per bene

        filesdb[index_to_update][6] = fh.getFileTable()

        self.setFilesdb(filesdb)

        self.socketclient.sendall("APAD" + numPeerParts_form)
        print "sent APAD" + numPeerParts_form + " to " + self.addrclient[0] + ":" + str(self.addrclient[1])

        print "num peer parts " + str(numPeerPart)

        self.printFilesdb()

        print ""