__author__ = 'GuiducciGrillandaLoPiccolo'

import kazaa_peer
import kazaa_peer_services
import kazaa_directory
#kazaa_directory_services non serve neanche

import socket
import hashlib #per calcolare l'md5 dei file
import copy
import string
import random
import time

class KazaaClient(object):

    def __init__(self): #AGGIORNATO -- DA CONTROLLARE

        """
        This method set the program parameters, such as IPP2P:P2P to allow others connection from/to other peers
        and IP address of Centralized Directory
        """

        # PEER

        #OS X
        self.my_IP = socket.gethostbyname(socket.gethostname())

        #Linux
        #self.my_IP = "address"

        my_IP_split = self.my_IP.split(".")
        IP_1 = '%(#)03d' % {"#" : int(my_IP_split[0])}
        IP_2 = '%(#)03d' % {"#" : int(my_IP_split[1])}
        IP_3 = '%(#)03d' % {"#" : int(my_IP_split[2])}
        IP_4 = '%(#)03d' % {"#" : int(my_IP_split[3])}
        self.my_IP_form = IP_1 + "." + IP_2 + "." + IP_3 + "." + IP_4 #IP formattato per bene

        self.my_port = 9999 # porta che io rendo disponibile per altri peer quando vogliono fare download da me
        self.my_port_form = '%(#)05d' % {"#" : int(self.my_port)} #porta formattata per bene

        self.dir_port = 8000 #da spefiche sarebbe l'80

        self.pickedRole = False
        self.logged = False #non sono loggato
        self.stop = False #non voglio uscire subito dal programma

        print ""

        # end of __init__ method

    # Definition of auxiliary methods

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


    def findneigh(self): #AGGIORNATO -- DA CONTROLLARE

        print "Find neighbours..."

        neigh_TTL = "0" #inizializzazione fittizia
        while int(neigh_TTL) < 1: #verifico che non venga inserito un valore non possibile
            neigh_TTL = raw_input("Insert neighbours TTL (min=1, typ=4): ")
        neigh_TTL_form = '%(#)02d' % {"#" : int(neigh_TTL)}
        pktID =  self.generate_pktID()

        queryService = kazaa_peer_services.Service()
        myQueryTable = queryService.getMyQueryTable()
        new_entry = []
        new_entry.append(pktID)
        new_entry.append(time.time())
        myQueryTable.append(new_entry)
        queryService.setMyQueryTable(myQueryTable)

        roleService = kazaa_peer_services.Service() #recupero il mio ruolo
        role = roleService.getRole()

        if role == "P": #se sono un peer mando la richiesta solo al superpeer

            superService = kazaa_peer_services.Service() #recupero il superpeer
            super = superService.getSuper()

            super_sock = self.openConn(super[0], super[1]) #passo ip e porta del superpeer
            super_sock.sendall("SUPE" + pktID + self.my_IP_form + self.my_port_form + neigh_TTL_form)
            print "sent SUPE" + pktID + self.my_IP_form + str(self.my_port_form) + str(neigh_TTL_form) + " to " + super[0] + ":" + str(super[1])
            self.closeConn(super_sock)

        else: #se sono un superpeer, mando la richiesta ai miei vicini superpeers

            nearService = kazaa_peer_services.Service()
            neighTable = nearService.getNeighTable()
            for n in range(0,len(neighTable)):
                neigh_sock = self.openConn(neighTable[n][0], neighTable[n][1]) #passo ip e porta
                neigh_sock.sendall("SUPE" + pktID + self.my_IP_form + self.my_port_form + neigh_TTL_form)
                print "sent SUPE" + pktID + self.my_IP_form + str(self.my_port_form) + str(neigh_TTL_form) + " to " + neighTable[n][0] + ":" + str(neighTable[n][1])
                self.closeConn(neigh_sock)

        #le risposte a questa richiesta mi arriveranno sulla porta P2P

        print ""

    # end of findNeigh method


    def login(self): #AGGIORNATO -- DA CONTROLLARE

        """
        login method control steps to join peer at P2P network
        """
        print "Login...\n"

        answer = raw_input("Do you want to change port? (Y/N) ") #sto parlando della porta messa a disposizione per gli altri peer
        if answer == "Y":
            self.my_port = raw_input("Port: ")
            self.my_port_form = '%(#)05d' % {"#" : int(self.my_port)} #porta formattata per bene

        superService = kazaa_peer_services.Service() #recupero il superpeer
        nextSuper = superService.getNextSuper()

        #invio LOGI al superpeer  (si tratta di un vero super nel caso io sia un peer, di me stesso nel caso io sia un superpeer)
        super_sock = self.openConn(nextSuper[0], nextSuper[1]) #passo ip e porta del superpeer
        super_sock.sendall("LOGI" + self.my_IP_form + self.my_port_form)
        print "sent LOGI" + self.my_IP_form + str(self.my_port_form) + " to " + nextSuper[0] + ":" + str(nextSuper[1])

        #ricevo ack ALGI
        ack = self.sockread(super_sock,20)
        print "received " + ack

        if ack[:4]=="ALGI":

            self.session_ID = ack[4:20]
            print "Session ID: " + self.session_ID + "\n"
            #non ho ancora controllato il SESSIONID

            # Check login non riuscito
            if self.session_ID=="0000000000000000":
                print "Login failed (0x16): try again!"
                self.logged=False #non sono loggato
            else:
                self.logged=True

                #aggiorno il super
                superService = kazaa_peer_services.Service() #recupero il superpeer
                superService.setSuper(nextSuper[0], nextSuper[1])

                #il login e' andato a buon fine, quindi mi metto in ascolto sulla porta specificata per il P2P
                self.myserver = kazaa_peer.ListenToPeers(self.my_IP_form, self.my_port_form)
                self.myserver.start()

        else:

            print "KO, ack ALGI parsing failed\n"
            self.logged=False #non sono loggato

        self.closeConn(super_sock)

        print ""

    # end of login method


    def nologin(self):
        """
        nologin method stop the program execution
        """
        print "You're about to exit the program"
        print "Bye!\n"
        self.stop = True
        # end of nologin method



    def addfile(self): #AGGIORNATO - DA CONTROLLARE
        """
        addfile method allows user to add a new file at Directory's Database
        """
        print "Add file...\n"

        superService = kazaa_peer_services.Service() #recupero il superpeer
        super = superService.getSuper()

        filename = raw_input("Insert the name of the file to add: ")
        self.checkfile(filename) #controllo l'esistenza del file nel percorso specificato
        md5file = self.md5_for_file(filename) #calcolo l'md5 del file
        filename_form = '%(#)0100s' % {"#" : filename} #formatto il nome del file

        #invio ADFF al superpeer
        super_sock = self.openConn(super[0], super[1]) #passo ip e porta del superpeer
        super_sock.sendall("ADFF" + self.session_ID + md5file + filename_form)
        print "sent ADFF" + self.session_ID + md5file + filename_form + " to " + super[0] + ":" + str(super[1])
        self.closeConn(super_sock)

        #mi salvo la corrispondenza tra filename e filemd5 nella mia tabellina fileTable
        #ma lo faccio solo se la riga non e' gia' presente
        fileService = kazaa_peer_services.Service()
        fileTable = fileService.getFileTable()

        notFound = True

        for i in range(0,len(fileTable)):
            if fileTable[i][1] == md5file:
                fileTable[i][0] = filename
                notFound = False

        if notFound: #il file non era presente nella tabellina fileTable, lo aggiungo

            newFile = []
            newFile.append(filename) #il filename non e' formattato
            newFile.append(md5file)
            fileTable.append(newFile)

        fileService.setFileTable(fileTable)

        print "fileTable"
        print fileService.getFileTable()

        # end of addfile method


    def delfile(self): #AGGIORNATO - DA CONTROLLARE
        """
        delfile method allows P2P user to remove a file that has previously shared into the network
        """
        print "Delete file...\n"

        superService = kazaa_peer_services.Service() #recupero il superpeer
        super = superService.getSuper()

        filename = raw_input("Insert the name of the file to delete: ")
        self.checkfile(filename) #controllo l'esistenza del file nel percorso specificato
        md5file = self.md5_for_file(filename) #calcolo l'md5 del file

        #invio ADFF al superpeer
        super_sock = self.openConn(super[0], super[1]) #passo ip e porta del superpeer
        super_sock.sendall("DEFF" + self.session_ID + md5file)
        print "sent DEFF" + self.session_ID + md5file + " to " + super[0] + ":" + str(super[1])
        self.closeConn(super_sock)

        # end of delfile method


    def findfile(self): #AGGIORNATO -- DA CONTROLLARE
        """
        this method allows at peer to specify a search string.
        If this matches a section of file name, the centralized directory says to peer the numbers of md5 checksum's
        occurrences and, for any of this, give the md5 hash, the file name and the copies number,
        while for any copy of file found in network lists IP & PORT of the peers that host searched file
        """
        print "Search file...\n"


        #chiedo stringa da cercare
        search = raw_input("Type a search string: ")
        search_form = '%(#)020s' % {"#" : search} #formatto la stringa di ricerca

        superService = kazaa_peer_services.Service() #recupero il superpeer
        super = superService.getSuper()

        #invio FIND al superpeer
        super_sock = self.openConn(super[0], super[1]) #passo ip e porta del superpeer
        super_sock.sendall("FIND" + self.session_ID + search_form)
        print "sent FIND" + self.session_ID + search_form + " to " + super[0] + ":" + str(super[1])

        #ricevo AFIN dalla directory
        ack = self.sockread(super_sock, 7) #leggo i primi 7B, poi il resto lo leggo dopo perche' non ha lunghezza fissa

        if ack[:4]=="AFIN":

            #print "OK, ack received\n" # DEBUG
            self.num_idmd5 = int(ack[4:7])
            print "Number of different md5: " + str(self.num_idmd5) + "\n"

            if self.num_idmd5 == 0:

                print "Sorry. No match found for your search"

            else:

                #creo gli array che mi serviranno dopo
                self.filemd5_down = []
                self.filename_down = []
                self.num_copy_down = []
                self.IPP2P_down = []
                self.PP2P_down = []
                tempIP = []
                tempPort = []

                # per ogni md5 trovato, eseguo un ciclo
                for i in range(0,self.num_idmd5): #i=numero di identificativo md5

                    #devo leggere altri byte ora
                    #ne leggo 119 perche' 119 e' la lunghezza del pezzo di cui so la lunghezza
                    ackmd5 = self.sockread(super_sock, 119)

                    self.filemd5_down.append(ackmd5[:16]) #lungo 16
                    nomedelfile = ackmd5[16:116]
                    nomedelfile = nomedelfile.strip(" ")
                    self.filename_down.append(nomedelfile) #lungo 100
                    numerodicopie = ackmd5[116:119]
                    numerodicopie = numerodicopie.lstrip("0")
                    self.num_copy_down.append(numerodicopie) #lungo 3
                    # ricordarsi che pero' parto dalla posizione 0 nell'array

                    print "md5 n." + str(int(i+1)) + ": " + self.filemd5_down[i] + ", filename: " + self.filename_down[i] + ", n.copy: " + self.num_copy_down[i]

                    # per ogni copia di quel particolare file-md5 [i], faccio un giro
                    for j in range(0,int(self.num_copy_down[i])): #j=numero di copia per quello stesso md5

                        ackcopy = self.sockread(super_sock, 20)
                        #di questi 20, 15 sono l'indirizzo, 5 sono la porta

                        print "    copy n.%d" % int(j+1) + ", identifier for download %d.%d" %(int(i+1),int(j+1))

                        tempIP.append(ackcopy[:15])

                        tempPort.append(ackcopy[15:20])

                        print "        IP: " + tempIP[j] + ", port: " + tempPort[j] + "\n"

                    self.IPP2P_down.append(copy.deepcopy(tempIP))
                    self.PP2P_down.append(copy.deepcopy(tempPort))

                    #ora svuoto l'array tempIP e tempPort cosi' sono pronta per la prossima volta

                    del tempPort[0:len(tempPort)]
                    del tempIP[0:len(tempIP)]


                self.closeConn(super_sock) #chiudo socket

                #arrivata qui ho stampato il "menu" con tutti i risultati della ricerca eseguita

                answer="Z" #la inizializzo ad una lettera a caso

                while answer!="Y" and answer!="N":

                    answer = raw_input("Do you want one of these copies? (Y/N): ")

                    if answer=="N":

                        print "You are being redirected to the main menu"
                        #non chiamo il metodo download() e continuo col mio normale flusso di lavoro
                        #ossia tornero' al menu principale

                    elif answer=="Y":

                        print "You are being redirected to the download section"
                        self.download()
                        #se l'utente non ha digitato ne' "Y" ne' "N" dovrebbe rifarmi la domanda un'altra volta
        else:

            print "KO, ack parsing failed\n"


    # end of find method


    def download(self): #AGGIORNATO -- DA CONTROLLARE
        """
        download method allow peer to make a download from any other peer into the network
        """
        print "Download section...\n"

        id_md5 = 0 #fake inizializzazione
        id_copy = 0


        while id_md5<1 or id_md5>int(self.num_idmd5) or id_copy<1 or id_copy>int(self.num_copy_down[id_md5-1]):

            choice = raw_input("Choose a copy to download: ")

            #mi dovrebbe arrivare dall'utente una cosa del tipo: "id_md5.id_copy"

            #splitto la sua risposta
            choice_split = choice.split(".")
            id_md5 = int(choice_split[0])
            id_copy = int(choice_split[1])

            #contro se la sua risposta e' in un formato giusto
            #ovvero controllo che id_md5 sia tra 1 e il numero di md5
            #e che id_copy sia tra 1 e numero di copie per quell'md5
            if id_md5<1 or id_md5>int(self.num_idmd5) or id_copy<1 or id_copy>int(self.num_copy_down[id_md5-1]):

                print "Warning: You mistyped your choice"

            else: #scelta corretta quindi inizio con il download vero e proprio


                #l'utente vuole scaricare la copia id_md5.id_copy
                #vado a recuperare le informazioni necessarie e le rinomino per comodita'
                filemd5 = self.filemd5_down[int(id_md5-1)]

                IPP2P = self.IPP2P_down[int(id_md5-1)][int(id_copy-1)]

                PP2P = self.PP2P_down[int(id_md5-1)][int(id_copy-1)]

                #mi salvo anche il nome del file cosi' uso quello per salvare il file nel mio pc
                filename = self.filename_down[int(id_md5-1)]

                #apro una socket verso il peer da cui devo scaricare
                #"iodown" perche' io faccio il download da lui

                try: # e' necessario tenere sotto controllo la connessione, perche' puo' disconnettersi il peer o non essere disponibile

                    iodown_socket = self.openConn(IPP2P, PP2P) #passo ip e porta

                except IOError: #IOError exception includes socket.error
                    print "Connection with " + IPP2P + "not available"
                else:
                    print "Connection with peer enstablished.\n"
                    #print "Download will start shortly! Be patient"

                    # SPEDISCO IL PRIMO MESSAGGIO
                    iodown_socket.sendall("RETR" + filemd5)

                    try:
                        # ricevo "ARET" dal peer
                        ack = self.sockread(iodown_socket, 10)
                    except IOError:
                        print "Connection error. The peer " + IPP2P + " is death\n"
                    else:

                        if ack[:4]=="ARET":

                            #pulisco il filename dagli spazi vuoti
                            filename_clean=str(filename).strip(' ')

                            fout = open(filename_clean,"ab") #a di append, b di binary mode

                            num_chunk = ack[4:10]

                            #pulisco il numero di chunks dagli 0
                            num_chunk_clean = str(num_chunk).lstrip('0')

                            for i in range (0,int(num_chunk_clean)): #i e' il numero di chunk

                                #devo leggere altri byte ora
                                #ne leggo 5 perche' 5 sono quelli che mi diranno poi quanto e' lungo il chunk
                                try:

                                    lungh_form = self.sockread(iodown_socket, 5)

                                    lungh = int(lungh_form) #converto in intero

                                    #devo leggere altri byte ora
                                    #ne leggo lungh perche' quella e' proprio la lunghezza del chunk

                                    data = self.sockread(iodown_socket, lungh)

                                    #lo devo mettere sul mio file che ho nel mio pc

                                    fout.write(data) #scrivo sul file in append

                                except IOError, expt:

                                    print "Connection or File-access error -> %s" % expt
                                    break
                                #ho finito di ricevere il file

                            fout.close() #chiudo il file perche' ho finito di scaricarlo

                            self.closeConn(iodown_socket) #chiudo socket

                        else:
                            print "KO, ack ARET parsing failed\n"
                            print "Download not available"


    # end of download method


    def logout(self): #AGGIORNATO -- DA CONTROLLARE

        """
        this method allows user to logout from P2P network
        """

        print "Logout...\n"

        superService = kazaa_peer_services.Service() #recupero il superpeer
        super = superService.getSuper()

        #invio LOGO al superpeer
        super_sock = self.openConn(super[0], super[1]) #passo ip e porta del superpeer
        super_sock.sendall("LOGO" + self.session_ID)
        print "sent LOGO" + self.session_ID + " to " + super[0] + ":" + str(super[1])

        #ricevo ALGO dal superpeer
        ack = self.sockread(super_sock,7) #controllare che siano davvero 3 quelli del num_delete
        print "received " + ack

        if ack[:4]=="ALGO":

            num_delete = ack[4:7]
            print "Number of deleted files: " + num_delete + "\n"

            self.myserver.setCheck()

            self.logged=False #non sono piu' loggato

        else :
            print "KO, ack parsing failed\n"
            self.logged=True #sono ancora loggato

        self.closeConn(super_sock)

        print ""

        # end of logout method


    def error(self):
        print "Option not valid: try again!\n"
        # end of error method


    def doYourStuff(self): #AGGIORNATO -- DA CONTROLLARE

        """
        This methods allow user to navigate into menu and logging in
        """

        if self.pickedRole==False:

            role = raw_input("Do you want to be peer or superpeer? (P/SP) ")
            self.pickedRole = True

            if role == "P": #non ho la tabella dei vicini, ma ho un superpeer

                super_ip = raw_input("Superpeer IP: ")
                super_port = raw_input("Superpeer port: ")

                superService = kazaa_peer_services.Service() #setto il super
                superService.setNextSuper(super_ip, super_port)


            else: #sono un superpeer, ho la tabella dei vicini e devo attivare il servizio di directory

                numNeigh = raw_input("How many neighbours do you want? ")

                neighService = kazaa_peer_services.Service()

                for i in range(0,int(numNeigh)):

                    neigh_ip = raw_input("Neighbour IP: ")
                    neigh_port = raw_input("Neighbour port: ")

                    neighService.addNeighbour(neigh_ip, neigh_port) #aggiungo vicino

                superService = kazaa_peer_services.Service() #setto me stesso come superpeer
                superService.setNextSuper(self.my_IP_form, self.dir_port)

                #in quanto superpeer mi metto in ascolto sulla porta 80
                self.mydirectory = kazaa_directory.ListenToPeers(self.my_IP_form, self.dir_port) #mio indirizzo, porta 80
                self.mydirectory.start()


            #memorizzo il ruolo scelto
            roleService = kazaa_peer_services.Service()
            roleService.setRole(role)


        if self.logged==False:

            print "Do you want to do login? (Y/N)\n" #TODO: eventualmente riorganizzare i gruppi di operazioni

        else: #allora sono loggato

            print "Choose between the following options, typing the number:\n"

            print "1. Search neighbours" #pensare in particolare questa funzione (prima cerco il neigh, poi logout, poi login nella nuova directory?)
            print "2. Add file"
            print "3. Delete file"
            print "4. Search and Download file"
            print "5. Logout\n"

        choice = raw_input("Choose an option: ")

        optNoLog = {

            'Y' : self.login,
            'N' : self.nologin,

        }

        optLog = {

            '1' : self.findneigh,
            '2' : self.addfile,
            '3' : self.delfile,
            '4' : self.findfile,
            '5' : self.logout

        }

        print ""

        if self.logged==False: #non sono loggato

            optNoLog.get(choice,self.error)() #se l'utente ha digitato un qualcosa che non esiste, viene chiamata error()

        else: #sono loggato

            optLog.get(choice,self.error)() #se l'utente ha digitato un qualcosa che non esiste, viene chiamata error()
            # end of doYourStuff method



if __name__ == "__main__":

    kc = KazaaClient() #inizializzazione


    while kc.stop==False:

        kc.doYourStuff() #stampa del menu ed esecuzione dell'opera