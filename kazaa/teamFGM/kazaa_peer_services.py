__author__ = 'GuiducciGrillandaLoPiccolo'

import kazaa_directory_services

import socket # networking module
import threading
import time


class Service():

    """
    This class implements all the methods that will be inherited by others classes
    """

    pktTable = [] #e' la tabella contenente gli ID dei pacchetti gia' ricevuti in passato

    rootTable = [] #tabella in cui ciascun peer tiene i suoi root (questi root possono essere sia peer che superpeer)

    dim_neighTable = 3
    neighTable = [] #tabella in cui il superpeer tiene i suoi vicini

    fileTable = [] #quando aggiungo un file nella directory, mi salvo qui l'md5 (filename e' il primo campo, filemd5 il secondo)
    #in questo modo, quando un altro peer mi chiedera' un file io riesco dall'md5 a risalire al nome del file

    myQueryTable = [] #tabella in cui io salvo le mie ricerche (pktid,time) in modo da verificare se sono passati 20 secondi

    role = [""] #mio ruolo: P oppure SP
    super = ["",0,0] #indirizzo, porta p2p, porta directory del mio attuale superpeer
    nextSuper = ["",0,0] #indirizzo, porta p2p, porta directory del superpeer che verra' utilizzato al prossimo login


    def getRole(self):
        return self.role[0]

    def setRole(self,role):
        self.role[0] = role

    def getSuper(self):
        return self.super

    def setSuper(self,IP,p2p_port,dir_port):
        self.super[0] = IP
        self.super[1] = p2p_port
        self.super[2] = dir_port

    def getNextSuper(self):
        return self.nextSuper

    def setNextSuper(self,IP,p2p_port,dir_port):
        self.nextSuper[0] = IP
        self.nextSuper[1] = p2p_port
        self.nextSuper[2] = dir_port

    def getPktTable(self):
        return self.pktTable

    def setPktTable(self,pktTable):
        self.pktTable = pktTable

    def getMyQueryTable(self):
        return self.myQueryTable

    def setMyQueryTable(self,myQueryTable):
        self.myQueryTable = myQueryTable

    def getRootTable(self):
        return self.rootTable

    def setRootTable(self,rootTable):
        self.rootTable = rootTable

    def getNeighDim(self):
        return self.dim_neighTable

    def setNeighDim(self,dim):
        self.dim_neighTable = dim

    def getNeighTable(self):
        return self.neighTable

    def setNeighTable(self,neighTable):
        self.neighTable = neighTable

    def getFileTable(self):
        return self.fileTable

    def setFileTable(self,fileTable):
        self.fileTable = fileTable

    def addRoot(self, IP, port):

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

        newline = []
        newline.append(IP_form)
        newline.append(port_form)
        self.rootTable.append(newline) #inserisco la nuova riga nella tabella dei root

        print self.rootTable


    def addNeighbour(self, IP, port): #questo metodo mi servira' solo per i superpeer (visto che i peer normali non hanno vicini)

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

        #rimuovo
        i = 0
        while i < len(pktTable):
            if i >= len(pktTable):
                break
            if now - pktTable[i][1] > 20: #se sono passati piu' di 20 secondi elimino la riga dalla tabella
                pktTable.pop(i)
            else:
                i = i+1

        self.setPktTable(pktTable)


    def checkPktAlreadySeen(self, pktID): #metodo per capire se il pacchetto e' passato sotto le mie mani negli ultimi 20 secondi

        pktTable = self.getPktTable()

        for i in range (0,len(pktTable)):

            if pktTable[i][0] == pktID: #se ho trovato il pacchetto
                return True

        #se sono uscita indenne dal ciclo (pacchetto non trovato)
        return False


class Query(threading.Thread, Service): #lo ricevo solo se sono un superpeer

    def __init__(self, socketclient, addrclient, my_IP_form, my_port_form):

        threading.Thread.__init__(self)

        # info sul peer che si connette, magari servono
        self.socketclient = socketclient
        self.addrclient = addrclient
        self.my_IP_form = my_IP_form
        self.my_port_form = my_port_form


    def searchFiles(self,search_string): #ATTENZIONE! deve essere la stessa che c'e' in kazaa_directory_services)

        lista_files = []

        #ricerca nella tabella filesdb di kazaa_directory_services
        #che e' la tabella dentro la quale ogni superpeer salva i file che sono stati aggiunti nella sua directory
        fileService = kazaa_directory_services.Service()
        filesdb = fileService.getFilesdb()

        for i in range(0,len(filesdb)):
            if filesdb[i][2].lower().find(search_string.lower()) != -1: #filesdb[i][2] e' il nome del file i-esimo
                new_file = []
                new_file.append(filesdb[i][0]) #sessionID
                new_file.append(filesdb[i][1]) #filemd5
                new_file.append(filesdb[i][2]) #filename
                lista_files.append(new_file)

        return lista_files #lista con i files che matchano la ricerca


    def run(self):

        #il pacchetto QUER lo ricevo solo se sono un superpeer

        query = self.sockread(self.socketclient,58)
        print "received QUER" + query + " from " + self.addrclient[0] + ":" + str(self.addrclient[1])
        pktID = query[:16]
        ipp2p = query[16:31] #ip del superpeer che ha effettuato la ricerca
        pp2p = query[31:36] #porta del superpeer che ha effettuato la ricerca
        ttl = query[36:38]
        ricerca_form = query[38:58]
        ricerca = ricerca_form.strip(" ")

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
                                                #sessionID, filemd5, filename

            if(len(files)==0):
                print "No file matches with query's search"


            else: #ho trovato almeno un file che matchi la ricerca
                print "Found #" + str(len(files)) + " files that meet query's search"

                fileService = kazaa_directory_services.Service()

                #mando un AQUE a chi ha mandato la query per ogni file trovato
                for f in range(0,len(files)): #f = indice riga (una riga=un file)

                    IPPort = fileService.getIPPortBySessID(files[f][0]) #dal sessionID ricavo array con IP e porta del peer
                    file_IP = IPPort[0]
                    file_port = IPPort[1]

                    filemd5 = files[f][1]
                    filename = files[f][2] #da formattare
                    filename_form = '%(#)0100s' % {"#" : filename} #formatto il nome del file

                    #invio l'ack al superpeer che ha effettuato la ricerca
                    neigh_sock = self.openConn(ipp2p, int(pp2p)) #passo ip e porta
                    neigh_sock.sendall("AQUE" + pktID + file_IP + file_port + filemd5 + filename_form)
                    print "sent AQUE" + pktID + file_IP + file_port + filemd5 + filename_form + " to " + ipp2p + ":" + str(pp2p)
                    self.closeConn(neigh_sock)

        print ""

    # end of run method

class AckQuery(threading.Thread, Service): #lo ricevo solo se sono un superpeer

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
        ipp2p = ack_query[16:31] #ip del peer che possiede il file
        pp2p = ack_query[31:36] #porta del peer che possiede il file
        filemd5 = ack_query[36:52]
        filename = ack_query[52:152]

        #ripristino il pezzo di codice seguente che in passato avevamo commentato
        #adesso dovrebbe funzionare tranquillamente :)
        myQueryTable = self.getMyQueryTable()

        for i in range(0,len(myQueryTable)):
            if pktID == myQueryTable[i][0]:
                if time.time() - myQueryTable[i][1] > 20: #se sono passati piu' di 20 secondi
                    print "AQUE request expired!"
                else:

                    #aggiorno la tabella dei match di kazaa_directory_services che sara' poi letta per costruire la risposta al FIND
                    matchService = kazaa_directory_services.Service()
                    matchTable = matchService.getMatchTable()

                    new_match = []
                    new_match.append(pktID)
                    new_match.append(ipp2p)
                    new_match.append(pp2p)
                    new_match.append(filemd5)
                    new_match.append(filename)

                    matchTable.append(new_match)

                    matchService.setMatchTable(matchTable)

        print ""

    # end of run method


class Super(threading.Thread, Service): #se sono un peer propago a super, se sono un superpeer propago ai vicini e rispondo

    def __init__(self, socketclient, addrclient, my_IP_form, my_port_form):

        threading.Thread.__init__(self)

        # info sul peer che si connette, magari servono
        self.socketclient = socketclient
        self.addrclient = addrclient
        self.my_IP_form = my_IP_form
        self.my_port_form = my_port_form


    def run(self):

        super = self.sockread(self.socketclient,38)
        print "received SUPE" + super + " from " + self.addrclient[0] + ":" + str(self.addrclient[1])
        pktID = super[:16]
        ipp2p = super[16:31]
        pp2p = super[31:36]
        ttl = super[36:38]

        self.cleanPktTable() #pulizia della tabella dei pacchetti

        if self.checkPktAlreadySeen(pktID): #se ho gia' ricevuto questo pacchetto
            print "Packet already received."

        else:
            self.addPktToTable(pktID) #aggiungo pacchetto alla tabella

            #procedo con tutto il resto

            role = self.getRole()

            #se il ttl e' maggiore di 1 devo ripropagare il pacchetto dopo aver decrementato il ttl
            #se tra i miei vicini c'e' anche chi ha effettuato la richiesta non devo mandarlo a lui
            if int(ttl)>1:

                #decremento il ttl prima di propagare il pacchetto
                ttl_decr = int(ttl) - 1
                ttl_form = '%(#)02d' % {"#" : int(ttl_decr)} #porta formattata per bene

                if role == "P": #se sono un peer, ripropago al mio super peer

                    super = self.super

                    if super[0] != ipp2p and super[1] != int(pp2p):

                        super_sock = self.openConn(super[0], super[1]) #passo ip e porta del superpeer
                        super_sock.sendall("SUPE" + pktID + ipp2p + pp2p + ttl_form)
                        print "sent SUPE" + pktID + ipp2p + str(pp2p) + ttl_form + " to " + super[0] + ":" + str(super[1])
                        self.closeConn(super_sock)

                else: #se sono superpeer, propago a tutti i miei vicini e rispondo con un ASUP

                    #propago
                    neighTable = self.getNeighTable()

                    for n in range(0,len(neighTable)): #n e' l'indice del vicino

                        if neighTable[n][0] != ipp2p and neighTable[n][1] != int(pp2p):

                            neigh_sock = self.openConn(neighTable[n][0], neighTable[n][1]) #passo ip e porta
                            neigh_sock.sendall("SUPE" + pktID + ipp2p + pp2p + ttl_form)
                            print "sent SUPE" + pktID + ipp2p + str(pp2p) + ttl_form + " to " + neighTable[n][0] + ":" + str(neighTable[n][1])
                            self.closeConn(neigh_sock)

            if role == "SP":
                #rispondo inviando ASUP a chi ha effettuato la ricerca
                neigh_sock = self.openConn(ipp2p, int(pp2p)) #passo ip e porta
                neigh_sock.sendall("ASUP" + pktID + self.my_IP_form + self.my_port_form)
                print "sent ASUP" + pktID + self.my_IP_form + self.my_port_form + " to " + ipp2p + ":" + str(pp2p)
                self.closeConn(neigh_sock)

        print ""

    # end of run method


class AckSuper(threading.Thread, Service): #se sono un peer aggiorno nextSuper, se sono un superpeer aggiorno tabella vicini

    def __init__(self, socketclient, addrclient, my_IP_form, my_port_form):

        threading.Thread.__init__(self)

        # info sul peer che si connette, magari servono
        self.socketclient = socketclient
        self.addrclient = addrclient
        self.my_IP_form = my_IP_form
        self.my_port_form = my_port_form


    def run(self):

        ack_supe = self.sockread(self.socketclient,36)
        print "received ASUP" + ack_supe + " from " + self.addrclient[0] + ":" + str(self.addrclient[1])
        pktID = ack_supe[:16]
        ipp2p = ack_supe[16:31]
        pp2p = ack_supe[31:36]

        myQueryTable = self.getMyQueryTable()

        for i in range(0,len(myQueryTable)):
            if pktID == myQueryTable[i][0]:
                if time.time() - myQueryTable[i][1] > 20: #se sono passati piu' di 20 secondi
                    print "ANEA request expired!"
                else:

                    role = self.getRole() #mi ricavo il mio ruolo

                    if role == "P": #sono un peer normale, mi e' arrivata la risposta da un superpeer

                        self.setNextSuper(ipp2p, pp2p, "8000") #aggiorno nextSuper con dati raccolti #TODO qui ho messo 8000 a mano, poi andra' sostituito con 80

                        print "New nextsuperpeer " + ipp2p + ":" + str(pp2p)

                    else: #sono un superpeer, aggiorno la tabella dei vicini

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
                #print "ho chiuso il file"
            except EOFError:
                print "You have read a EOF char"

        print ""


    # end of run method