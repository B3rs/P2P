__author__ = 'GuiducciGrillandaLoPiccolo'

import socket # networking module
import threading
import os
import re
import time
import hashlib #per calcolare l'md5 dei file


class Service():

    """
    This class implements all the methods that will be inherited by others classes
    """

    pktTable = [] #e' la tabella contenente gli ID dei pacchetti gia' ricevuti in passato
    #tutte le classi che estendono Service possono accedervi ed e' come se fosse una tabella fatta sul db

    dim_neighTable = 3 #lo inizializzo a zero
    neighTable = []

    fileTable = [] #tabella in cui salvo la corrispondenza tra nome file e suo md5
    #la salvo solo quando mi arriva una query di ricerca a cui io rispondo che ho il file e mando l'md5
    #gia' che ci sono lo salvo in questa tabellina cosi' poi quando il peer mi chiedera' di fare il download
    #io faro' in frettissima a recuperarlo
    #filename e' il primo campo, filemd5 il secondo

    downTable = []

    myQueryTable = [] #tabella in cui io salvo le mie ricerche (pktid,time)

    def getPktTable(self): #prova
        return self.pktTable

    def setPktTable(self,pktTable): #prova
        self.pktTable = pktTable

    def getMyQueryTable(self): #prova
            return self.myQueryTable

    def setMyQueryTable(self,myQueryTable): #prova
        self.myQueryTable = myQueryTable

    def getNeighDim(self):
        return self.dim_neighTable

    def setNeighDim(self,dim):
        self.dim_neighTable = dim

    def getNeighTable(self): #prova
        return self.neighTable

    def setNeighTable(self,neighTable): #prova
        self.neighTable = neighTable

    def getFileTable(self): #prova
        return self.fileTable

    def setFileTable(self,fileTable): #prova
        self.fileTable = fileTable

    def getDownTable(self): #prova
            return self.downTable

    def setDownTable(self,downTable): #prova
        self.downTable = downTable

    def addNeighbour(self, IP, port):


        """
        This method add a neighbour to neighTable. If this table is empty, provides to add the neighbour given by
        parameters, specifying his IP and Port.
        Otherwise, new neighbour is added after deleting the oldest neighbour in the table
        """

        #salvo nella tabella gli IP e le porte gia' formattate per bene

        #formatto IP
        IP_split = IP.split(".")
        IP_1 = '%(#)03d' % {"#" : int(IP_split[0])}
        IP_2 = '%(#)03d' % {"#" : int(IP_split[1])}
        IP_3 = '%(#)03d' % {"#" : int(IP_split[2])}
        IP_4 = '%(#)03d' % {"#" : int(IP_split[3])}
        IP_form = IP_1 + "." + IP_2 + "." + IP_3 + "." + IP_4 #IP formattato per bene

        #formatto porta
        port_form = '%(#)05d' % {"#" : int(port)} #porta formattata per bene


        if len(self.neighTable) < self.getNeighDim(): #se tabella non ancora tutta piena
            newline = []
            newline.append(IP_form)
            newline.append(port_form)
            newline.append(time.time()) #numero di secondi dall'epoca
            self.neighTable.append(newline) #inserisco la nuova riga nella tabella dei vicini
        elif len(self.neighTable) == self.getNeighDim() : #tabella piena
            # devo eliminare qualche vicino memorizzato
            to_replace = 0
            oldest=self.neighTable[to_replace][2] #inizializzo la variabile "piu' vecchio alla prima entry della tabella
            for i in range(0,len(self.neighTable)): # i e' un elemento di neighTable
                tmp=self.neighTable[i][2] #tmp diventa l'orario
                if tmp < oldest :
                    oldest = tmp
                    to_replace = i
                # ho individuato l'elemento che non uso da piu' tempo e lo rimpiazzo con un neighbour nuovo
            self.neighTable[to_replace][0]= IP_form
            self.neighTable[to_replace][1]= port_form
            self.neighTable[to_replace][2]= time.time()
        else:
            print "An error occured in neighTable handling"

        print self.neighTable

    #end of addNeighbour method


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

    def addPktToTable(self, pktID): #scrivo sulla tabella che ho esaminato il pacchetto

        pktTable = self.getPktTable()

        newPkt = []
        newPkt.append(pktID)
        newPkt.append(time.time())
        pktTable.append(newPkt)
        self.setPktTable(pktTable)


    def cleanPktTable (self):
        """
        This method provides to clean pktTable, by deleting all packets that was added in  last 300 seconds
        after receiving pktID (or his creation)
        """
        #faccio la pulizia della tabella dei pacchetti
        #eliminando quelli piu' vecchi di 300 secondi
        now = time.time()

        pktTable = self.getPktTable()

        for i in range(0,len(pktTable)):

            if i>=len(pktTable):
                break

            if now - pktTable[i][1] > 300: #se sono passati piu' di 300 secondi elimino la riga dalla tabella

                pktTable.pop(i)

        self.setPktTable(pktTable)


    def checkPktAlreadySeen(self, pktID): #metodo per capire se il pacchetto e' passato sotto le mie mani negli ultimi 300 secondi

        pktTable = self.getPktTable()

        for i in range (0,len(pktTable)):

            if pktTable[i][0] == pktID: #se ho trovato il pacchetto
                return True

        #se sono uscita indenne dal ciclo (pacchetto non trovato)
        return False


class Query(threading.Thread, Service): #ereditarieta' multipla

    def __init__(self, socketclient, addrclient, my_IP_form, my_port_form):

        threading.Thread.__init__(self)

        # info sul peer che si connette, magari servono
        self.socketclient = socketclient
        self.addrclient = addrclient
        self.my_IP_form = my_IP_form
        self.my_port_form = my_port_form


    def searchFiles(self,search_string):

        lista_files = []

        dir = "/Users/Francesca/PycharmProjects/P2P/gnutella/teamFGM" #FRE
        #dir = "/Users/ingiulio/P2P/gnutella/teamFGM" #GIU
        #dir = "/home/Dropbox/Git_Pycharm/P2P/gnutella/teamFGM" #MAU

        dirEntries = os.listdir(dir)
        for entry in dirEntries:
            if entry.lower().find(search_string.lower()) != -1:
                lista_files.append(entry)
        return lista_files


    def run(self):

        query = self.sockread(self.socketclient,58)
        print "received QUER" + query + " from " + self.addrclient[0] + ":" + str(self.addrclient[1])
        pktID = query[:16]
        ipp2p = query[16:31]
        pp2p = query[31:36]
        ttl = query[36:38]
        ricerca_form = query[38:58]
        ricerca = ricerca_form.strip(" ") #pulisco la stringa dagli spazi

        self.cleanPktTable() #pulizia della tabella dei pacchetti

        if self.checkPktAlreadySeen(pktID): #se ho gia' ricevuto questo pacchetto
            print "Packet already received."
        else:
            self.addPktToTable(pktID) #aggiungo pacchetto alla tabella

            #procedo con tutto il resto

            #se il ttl e' maggiore di 1 devo ripropagare il pacchetto dopo aver decrementato il ttl
            #se tra i miei vicini c'e' anche chi ha effettuato la ricerca non devo mandarlo a lui
            if int(ttl)>1:

                #decremento il ttl prima di propagare il pacchetto
                ttl_decr = int(ttl) - 1
                ttl_form = '%(#)02d' % {"#" : int(ttl_decr)} #porta formattata per bene

                neighTable = self.getNeighTable()

                for n in range(0,len(neighTable)): #n e' l'indice del vicino

                    if neighTable[n][0] != ipp2p and neighTable[n][1] != int(pp2p):

                        neigh_sock = self.openConn(neighTable[n][0], neighTable[n][1]) #passo ip e porta
                        neigh_sock.sendall("QUER" + pktID + ipp2p + pp2p + ttl_form + ricerca_form)
                        print "sent QUER" + pktID + ipp2p + pp2p + ttl_form + ricerca_form + " to " + neighTable[n][0] + ":" + str(neighTable[n][1])
                        self.closeConn(neigh_sock)

            #in ogni caso cerco tra i miei files se ne ho uno che matcha la ricerca
            files = self.searchFiles(ricerca) #files = lista di files che matchano la ricerca

            if(len(files)==0):
                print "No file matches with query's search" #TODO debug


            else: #ho trovato almeno un file che matchi la ricerca
                print "Found #" + str(len(files)) + " files that meet query's search" #TODO debug

                #mando un aque a chi ha mandato la query per ogni file trovato
                for f in range(0,len(files)): #f = indice file

                    #files[f] dovrebbe essere il nome del file
                    filename = files[f]
                    filename_form = '%(#)0100s' % {"#" : filename} #formatto il nome del file

                    #calcolo l'md5 del file
                    filemd5 = self.md5_for_file(filename)

                    #siccome e' probabile che poi il peer vorra' fare il download da me
                    #mi salvo la corrispondenza tra filename e filemd5 nella mia tabellina fileTable
                    #ma lo faccio solo se la riga non e' gia' presente
                    fileTable = self.getFileTable()

                    notFound = True

                    for i in range(0,len(fileTable)):
                        if filemd5 == fileTable[i][1]:
                            notFound = False

                    if notFound: #il file non era presente nella tabellina fileTable, lo aggiungo

                        newFile = []
                        newFile.append(filename) #il filename non e' formattato
                        newFile.append(filemd5)
                        fileTable.append(newFile)
                        self.setFileTable(fileTable)
                        #print self.getFileTable()

                    #invio l'ack a chi ha effettuato la ricerca
                    neigh_sock = self.openConn(ipp2p, int(pp2p)) #passo ip e porta
                    neigh_sock.sendall("AQUE" + pktID + self.my_IP_form + self.my_port_form + filemd5 + filename_form)
                    print "sent AQUE" + pktID + self.my_IP_form + self.my_port_form + filemd5 + filename_form + " to " + ipp2p + ":" + str(pp2p)
                    self.closeConn(neigh_sock)

        print ""

    # end of run method

class AckQuery(threading.Thread, Service):

    def __init__(self, socketclient, addrclient, my_IP_form, my_port_form):

        threading.Thread.__init__(self)

        # info sul peer che si connette, magari servono
        self.socketclient = socketclient
        self.addrclient = addrclient
        self.my_IP_form = my_IP_form
        self.my_port_form = my_port_form


    def run(self):

        ack_query = self.sockread(self.socketclient,152)
        print "received AQUE" + ack_query + " from " + self.addrclient[0] + ":" + str(self.addrclient[1])
        pktID = ack_query[:16]
        ipp2p = ack_query[16:31]
        pp2p = ack_query[31:36]
        filemd5 = ack_query[36:52]
        filename = ack_query[52:152]
        filename = filename.strip(" ") #pulisco la stringa dagli spazi

        myQueryTable = self.getMyQueryTable()

        for i in range(0,len(myQueryTable)):
            if pktID == myQueryTable[i][0]:
                if time.time() - myQueryTable[i][1] > 300: #se sono passati piu' di 300 secondi
                    print "AQUE request expired!"
                else:
                    downTable = self.getDownTable()

                    if not len(downTable): #se tabella vuota
                        id = 1
                    else:
                        id = len(downTable) + 1

                    print "Download code: " + str(id)

                    new_ack = []
                    new_ack.append(id)
                    new_ack.append(ipp2p)
                    new_ack.append(pp2p)
                    new_ack.append(filemd5)
                    new_ack.append(filename)
                    new_ack.append(pktID)

                    downTable.append(new_ack)

                    self.setDownTable(downTable)

        print ""

    # end of run method


class Near(threading.Thread, Service):

    def __init__(self, socketclient, addrclient, my_IP_form, my_port_form):

        threading.Thread.__init__(self)

        # info sul peer che si connette, magari servono
        self.socketclient = socketclient
        self.addrclient = addrclient
        self.my_IP_form = my_IP_form
        self.my_port_form = my_port_form


    def run(self):

        near = self.sockread(self.socketclient,38)
        print "received NEAR" + near + " from " + self.addrclient[0] + ":" + str(self.addrclient[1])
        pktID = near[:16]
        ipp2p = near[16:31]
        pp2p = near[31:36]
        ttl = near[36:38]

        self.cleanPktTable() #pulizia della tabella dei pacchetti

        if self.checkPktAlreadySeen(pktID): #se ho gia' ricevuto questo pacchetto
            print "Packet already received."

        else:
            self.addPktToTable(pktID) #aggiungo pacchetto alla tabella

            #procedo con tutto il resto

            #se il ttl e' maggiore di 1 devo ripropagare il pacchetto dopo aver decrementato il ttl
            #se tra i miei vicini c'e' anche chi ha effettuato la richiesta non devo mandarlo a lui
            if int(ttl)>1:

                #decremento il ttl prima di propagare il pacchetto
                ttl_decr = int(ttl) - 1
                ttl_form = '%(#)02d' % {"#" : int(ttl_decr)} #porta formattata per bene

                neighTable = self.getNeighTable()

                for n in range(0,len(neighTable)): #n e' l'indice del vicino

                    if neighTable[n][0] != ipp2p and neighTable[n][1] != int(pp2p):

                        neigh_sock = self.openConn(neighTable[n][0], neighTable[n][1]) #passo ip e porta
                        neigh_sock.sendall("NEAR" + pktID + ipp2p + pp2p + ttl_form)
                        print "sent NEAR" + pktID + ipp2p + pp2p + ttl_form + " to " + neighTable[n][0] + ":" + str(neighTable[n][1])
                        self.closeConn(neigh_sock)


            #rispondo alla richiesta invio l'ack AQUE a chi ha effettuato la ricerca
            neigh_sock = self.openConn(ipp2p, int(pp2p)) #passo ip e porta
            neigh_sock.sendall("ANEA" + pktID + self.my_IP_form + self.my_port_form)
            print "sent ANEA" + pktID + self.my_IP_form + self.my_port_form + " to " + ipp2p + ":" + str(pp2p)
            self.closeConn(neigh_sock)

        print ""

    # end of run method


class AckNear(threading.Thread, Service):

    def __init__(self, socketclient, addrclient, my_IP_form, my_port_form):

        threading.Thread.__init__(self)

        # info sul peer che si connette, magari servono
        self.socketclient = socketclient
        self.addrclient = addrclient
        self.my_IP_form = my_IP_form
        self.my_port_form = my_port_form


    def run(self):

        ack_near = self.sockread(self.socketclient,36)
        print "received ANEA" + ack_near + " from " + self.addrclient[0] + ":" + str(self.addrclient[1])
        pktID = ack_near[:16]
        ipp2p = ack_near[16:31]
        pp2p = ack_near[31:36]

        myQueryTable = self.getMyQueryTable()

        for i in range(0,len(myQueryTable)):
            if pktID == myQueryTable[i][0]:
                if time.time() - myQueryTable[i][1] > 300: #se sono passati piu' di 300 secondi
                    print "ANEA request expired!"
                else:

                    neighTable = self.getNeighTable()

                    toadd=True

                    for i in range(0,len(neighTable)):
                        if ipp2p == neighTable[i][0] and pp2p == neighTable[i][1]: #vicino gia' presente
                            toadd = False
                            break
                        elif ipp2p == neighTable[i][0] and pp2p != neighTable[i][1]: #ip presente, ma porta diversa --> aggiorno porta
                            neighTable[i][1] = pp2p
                            toadd = False
                            break
                        else: #vicino non esistente
                            toadd = True
                    if toadd == True:

                        self.addNeighbour(ipp2p, pp2p)
                        print "Added neighbour " +  ipp2p + ":" + str(pp2p)

                    self.setNeighTable(neighTable)

        print ""

    # end of run method


class Upload(threading.Thread, Service):

    def __init__(self, socketclient, addrclient, IP_form, port_form):

        threading.Thread.__init__(self)

        # info sul peer che si connette, magari servono
        self.socketclient = socketclient
        self.addrclient = addrclient
        self.IP_form = IP_form
        self.port_form = port_form

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

        download = self.sockread(self.socketclient,16)
        print "received RETR" + download + " from " + self.addrclient[0] + ":" + str(self.addrclient[1])
        md5tofind = download[:16]

        chunk_dim = 128 # specifica la dimensione in byte del chunk (fix)

        fileTable = self.getFileTable()

        # ricerca della corrispondenza
        for i in fileTable:
            if i[1] == md5tofind:
                filename = i[0]

        # dividere il file in chuncks

        try :
            file = open(filename, "rb")
        except Exception,expt:
            print "Error: %s" %expt + "\n"
            print "An error occured, file upload unavailable for peer " + self.addrclient[0] + ":" + str(self.addrclient[1]) + "\n"
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

                        #print chunk_dim_form
                        self.socketclient.sendall(str(chunk_dim_form) + buff)
                        chunk_sent = chunk_sent +1
                        buff = file.read(chunk_dim)
                    except IOError: #this exception includes the socket.error child!
                        print "Connection error due to the death of the peer!!!\n"
                if len(buff) != 0:
                    chunk_last_form = '%(#)05d' % {"#" : len(buff)}
                    self.socketclient.sendall(chunk_last_form + buff)
                print "End of upload of " + filename + " to " + self.addrclient[0] + ":" + str(self.addrclient[1])
                file.close()
                #print "ho chiuso il file" #TODO debug
            except EOFError:
                print "You have read a EOF char"

        print ""


    # end of run method