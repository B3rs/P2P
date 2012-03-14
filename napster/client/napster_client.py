__author__ = 'ingiulio'

#from napster_client_threads import ListenToPeers

import socket
import hashlib #per calcolare l'md5 dei file
import time # per le funzioni di wait -> uso le sleep, che mi freezano il processo
import sys # mi consente di usare il metodo sys.stdout.write per scrivere sulla stessa riga


class NapsterClient(object):

    def __init__(self):

        """
        This method set the program parameters, such as IPP2P:P2P to allow others connection from/to other peers
        and IP address of Centralized Directory
        """
        print "Init Napster client\n"

        # DIRECTORY
        self.dir_host = "192.168.1.115" # indirizzo della directory
        self.dir_port = 9999 # porta di connessione alla directory - DA SPECIFICHE: sarebbe la 80
        self.dir_addr = (self.dir_host, self.dir_port)

        # PEER
        self.myP2P_port = 6500 # porta che io rendo disponibile per altri peer quando vogliono fare download da me

        self.logged = False #non sono loggato
        self.stop = False #non voglio uscire subito dal programma
        self.fileTable = []
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
        print "Funzione che calcola l'md5 di un file" #TODO: DEBUG MODE

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
            print md5.digest()
            print md5.hexdigest()
            return md5.digest()
    # end of md5_for_file method


    def checkfile(self, filename):
        """
        this method verify the presence of file into file system through his path, specified as parameter in function call
        """
        try :
            f = open(filename)
        except Exception, expt :
            print "Peer can't verify file presence -> %s" % expt + "\n"
        else:
            f.close()
    # end of checkfile method

    def login(self):

        """
        login method control steps to join peer at P2P network
        """
        print "Login...\n"

        #mi connetto alla directory tramite la socket self.dir_socket
        try:
            self.dir_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.dir_socket.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
            self.dir_socket.connect(self.dir_addr)
        except IOError, expt: #IOError exception includes a sub-exception socket.error
            print "Error occured in Connection with Directory -> %s" % expt + "\n"
        else:
            print "Connection with directory enstablished\n"

            # Formattazione indirizzo IP per invio alla directory
            self.my_IP = self.dir_socket.getsockname()[0] #IP non ancora formattato
            my_IP_split = self.my_IP.split(".")
            IP_1 = '%(#)03d' % {"#" : int(my_IP_split[0])}
            IP_2 = '%(#)03d' % {"#" : int(my_IP_split[1])}
            IP_3 = '%(#)03d' % {"#" : int(my_IP_split[2])}
            IP_4 = '%(#)03d' % {"#" : int(my_IP_split[3])}
            self.myIPP2P_form = IP_1 + "." + IP_2 + "." + IP_3 + "." + IP_4 #IP formattato per bene

            # Formattazione porta
            self.myPP2P_form = '%(#)05d' % {"#" : int(self.myP2P_port)} #porta formattata per bene

            # CREO LA SOCKET PER GLI ALTRI PEERS
            #myserver = ListenToPeers()
            #myserver.start(self.my_IP,self.myP2P_port) # controllare se il passaggio dei parametri e' corretto

            # SPEDISCO IL PRIMO MESSAGGIO
            self.dir_socket.send("LOGI" + self.myIPP2P_form + self.myPP2P_form)


            # Acknowledge "ALGI" dalla directory
            ack = self.dir_socket.recv(20)
            print ack

            if ack[:4]=="ALGI":

                print "OK, ack received\n"
                self.session_ID = ack[4:20]
                print "Session ID: " + self.session_ID + "\n"
                #non ho ancora controllato il SESSIONID

                # Check login non riuscito
                if self.session_ID=="0000000000000000":
                    print "Login failed: try again!"
                    self.dir_socket.close()
                    self.logged=False #non sono loggato
                else:
                    self.logged=True
                    #DownloadMe().start() #thread che gestisce il download da parte dei peer


            else :
                print "KO, ack parsing failed\n"
                self.logged=False #non sono loggato
        # end of exception's else
    # end of login method


    def nologin(self):
        """
        nologin method stop the program execution
        """
        sys.stdout.write("You're about to exit the program")
        self.dots()
        print "Bye!\n"
        self.stop = True
    # end of nologin method



    def addfile(self):
        """
        addfile method allows user to add a new file at Directory's Database
        """
        print "Add file...\n"

        filename = raw_input("Insert the name of the file to add: ")

        md5file = self.md5_for_file(filename) #calcolo l'md5 del file

        filename_form = '%(#)0100s' % {"#" : filename} #formatto il nome del file

        print "Filename in format '%100s': " + filename_form

        self.checkfile(filename) #soluzione proposta da maury

        # SPEDISCO IL PACCHETTO
        self.dir_socket.send("ADDF" + self.session_ID)
        self.dir_socket.send(md5file)
        self.dir_socket.send(filename_form)

        # Acknowledge "AADD" dalla directory
        ack = self.dir_socket.recv(7)
        print ack

        if ack[:4]=="AADD":
            print "OK, ack received\n" # DEBUG
            num_copy = ack[4:7]
            print "Number of copies: " + num_copy + "\n"

            # Check num copies
            if int(num_copy) < 1:
                print "Central Directory hasn't add your file"
            else:
                print "Added copy"
                # registro nella mia personale "tabella" il file aggiunto, e il suo md5
                fileadded = [filename,md5file]
                self.fileTable.append(fileadded)
        else :
            print "KO, ack parsing failed\n"
            print "Adding file failed!\n"
    # end of addfile method


    def delfile(self):
        """
        delfile method allows P2P user to remove a file that has previously shared into the network
        """
        print "Delete file...\n"

        filename = raw_input("Insert the name of the file to delete: ")

        md5file = self.md5_for_file(filename) #calcolo l'md5 del file

        # SPEDISCO IL PACCHETTO
        self.dir_socket.send("DELF" + self.session_ID + md5file)

        # Acknowledge "ADEL" from directory
        ack = self.dir_socket.recv(7)
        print ack

        if ack[:4]=="ADEL":
            print "OK, ack  'ADEL' received\n" # DEBUG
            num_copy = ack[4:7]
            print "Number of copies left: " + num_copy + "\n"

            # Check num copies
            if int(num_copy) < 0:
                print "Warning: an error occured during file deleting\n"
            else:
                print "The specified copy has been removed\n"
        else :
            print "KO, ack parsing failed\n"
            print "Removing file failed\n"
    # end of delfile method

    def find(self):
        """
        this method allows at peer to specify a search string.
        If this matches a section of file name, the centralized directory says to peer the numbers of md5 checksum's
        occurrences and, for any of this, give the md5 hash, the file name and the copies number,
        while for any copy of file found in network lists IP & PORT of the peers that host searched file
        """
        print "Find...\n"

        search = raw_input("Type a search string: ")

        search_form = '%(#)020s' % {"#" : search} #formatto la stringa di ricerca

        # SPEDISCO IL PACCHETTO
        self.dir_socket.send("FIND" + self.session_ID + search_form)

        # Acknowledge "AFIN" from directory
        ack = self.dir_socket.recv(7) #leggo i primi 7B, poi il resto lo leggo dopo perche' non ha lunghezza fissa
        print ack

        if ack[:4]=="AFIN":

            print "OK, ack received\n" # DEBUG
            num_idmd5 = ack[4:7]
            print "Number of different md5: " + num_idmd5 + "\n"

            if num_idmd5==0:

                print "Sorry. No match found for your search"

            else:

                #creo gli array che mi serviranno dopo
                #array:
                self.filemd5_down = []
                self.filename_down = []
                self.num_copy_down = []
                #matrici:
                self.IPP2P_down = [[]]
                self.PP2P_down = [[]]
                #TODO: verificare che le matrici si istanzino davvero cosi'

                for i in range(1,num_idmd5): #i=numero di identificativo md5

                    #devo leggere altri byte ora
                    #ne leggo 119 perche' 119 e' la lunghezza del pezzo di cui so la lunghezza
                    ackmd5 = self.dir_socket.recv(119)
                    print ackmd5

                    print "md5 n." + i

                    self.filemd5_down[i] = ackmd5[:16] #lungo 16
                    self.filename_down[i] = ackmd5[16:116] #lungo 100
                    self.num_copy_down[i] = ackmd5[116:119] #lungo 3
                    print "md5 n." + i + self.filemd5_down[i] + self.filename_down[i] + self.num_copy_down[i]
                    #la lunghezza di questo pezzo e' sempre 119

                    for j in range(1,self.num_copy_down[i]): #j=numero di copia per quello stesso md5

                        #devo leggere altri byte ora
                        #ne leggo 20*numero_di_copie
                        #perche' per ogni copia devo leggere 20 byte

                        ackcopy = self.dir_socket.recv(20*self.num_copy_down[i])
                        print ackcopy

                        print "copy n." + j
                        print "identificativo con cui scaricarla " + i + "." + "j"

                        self.IPP2P_down[i][j] = ackcopy[:15] #lungo 15
                        self.PP2P_down[i][j] = ackcopy[15:20] #lungo 5
                        print "    copy n." + i + self.IPP2P_down[i][j] + self.PP2P_down[i][j]
                        #la lunghezza di questo pezzo e' 20*num_copy[i]


                #arrivata qui ho stampato il "menu" con tutti i risultati della ricerca eseguita

                answer="Z" #la inizializzo ad una lettera a caso

                while answer!="Y" and answer!="N":

                    answer = raw_input("Vuoi scaricare una di queste copie? (Y/N)")

                    if answer=="N":

                        sys.stdout.write("You are being redirected to the main menu")
                        self.dots()
                        #non chiamo il metodo download() e continuo col mio normale flusso di lavoro
                        #ossia tornero' al menu principale

                    elif answer=="Y":

                        sys.stdout.write("You are being redirected to the download section")
                        self.dots()

                        self.download()

                    #se l'utente non ha digitato ne' "Y" ne' "N" dovrebbe rifarmi la domanda un'altra volta


        else:

            print "KO, ack parsing failed\n"
    # end of find method


    def download(self):
        """
        download method allow peer to make a download from any other peer into the network
        """
        print "Download section...\n"

        choice = "0.0"

        while id_md5<1 or id_md5>self.num_idmd5 or id_copy<1 or id_copy>self.num_copy_down[i]:

            choice = raw_input("Choose a copy to download: ")

            #mi dovrebbe arrivare dall'utente una cosa del tipo: "id_md5.id_copy"

            #splitto la sua risposta
            choice_split = choice.split(".")
            id_md5 = int(choice_split[0])
            id_copy = int(choice_split[1])

            #contro se la sua risposta e' in un formato giusto
            #ovvero controllo che id_md5 sia tra 1 e il numero di md5
            #e che id_copy sia tra 1 e numero di copie per quell'md5

            if id_md5<1 or id_md5>self.num_idmd5 or id_copy<1 or id_copy>self.num_copy_down[i]:

                print "Warning: You mistyped your choice"

            else: #scelta corretta quindi inizio con il download vero e proprio


                #l'utente vuole scaricare la copia id_md5.id_copy
                #vado a recuperare le informazioni necessarie e le rinomino per comodita'
                filemd5 = self.filemd5_down[id_md5]
                IPP2P = self.IPP2P_down[id_md5][id_copy]
                PP2P = self.P2P_down[id_md5][id_copy]
                #mi salvo anche il nome del file cosi' uso quello per salvare il file nel mio pc
                filename = self.filename_down[id_md5]

                #apro una socket verso il peer da cui devo scaricare
                #"iodown" perche' io faccio il download da lui
                iodown_host = IPP2P
                iodown_port = int(PP2P)
                iodown_addr = iodown_host, iodown_port
                #TODO: inserire controllo eccezioni per la caduta della connessione col peer
                iodown_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                iodown_socket.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
                iodown_socket.connect(iodown_addr)
                print "Connection with peer enstablished.\n"
                print "Download will start shortly! Be patient"

                # SPEDISCO IL PRIMO MESSAGGIO
                iodown_socket.send("RETR" + filemd5)

                # Acknowledge "ARET" dal peer
                ack = iodown_socket.recv(10)
                print ack

                if ack[:4]=="ARET":

                    print "Download is coming..."

                    fout = open(filename,"ab") #a di append

                    num_chunk = ack[4:10]
                    print "The #chunk is " + num_chunk + "\n"

                    for i in range (1,num_chunk): #i e' il numero di chunk
                        print "Watching chunk number " + str(i) + "\n"

                        #devo leggere altri byte ora
                        #ne leggo 5 perche' 5 sono quelli che mi diranno poi quanto e' lungo il chunk

                        lungh = int(iodown_socket.recv(5))
                        print lungh

                        #devo leggere altri byte ora
                        #ne leggo lungh perche' quella e' proprio la lunghezza del chunk

                        data = iodown_socket.recv(5)
                        print data

                        #lo devo mettere sul mio file che ho nel mio pc

                        fout.write(data) #scrivo sul file in append

                    #ho finito di ricevere il file
                    fout.close() #chiudo il file perche' ho finito di scaricarlo


                    #dopo il download comunico alla directory che ho fatto questo download
                    #come al solito devo mandargli IP e porta del peer da cui ho scaricato formattati

                    # Formattazione indirizzo IP peer per invio alla directory
                    IPP2P_split = IPP2P.split(".")
                    IPP2P_1 = '%(#)03d' % {"#" : int(IPP2P_split[0])}
                    IPP2P_2 = '%(#)03d' % {"#" : int(IPP2P_split[1])}
                    IPP2P_3 = '%(#)03d' % {"#" : int(IPP2P_split[2])}
                    IPP2P_4 = '%(#)03d' % {"#" : int(IPP2P_split[3])}
                    IPP2P_form = IPP2P_1 + "." + IPP2P_2 + "." + IPP2P_3 + "." + IPP2P_4 #IP formattato per bene

                    # Formattazione porta
                    PP2P_form = '%(#)05d' % {"#" : int(PP2P)} #porta formattata per bene

                    self.dir_socket.send("RREG" + self.session_ID + filemd5 + IPP2P_form + PP2P_form)

                    # Acknowledge "ARRE" dalla directory
                    ack = self.dir_socket.recv(9)
                    print ack

                    if ack[:4]=="ARRE":

                        print "OK, ack received\n" # DEBUG
                        num_down = ack[4:9]
                        print "Number of download: " + num_down + "\n"

                        # Check num downloads
                        if int(num_down) < 1:
                            print "Warning: Verified a mismatch in the number of download"
                        else:
                            print "ok"


                    else :
                        print "KO, ack parsing failed\n"
                        print "Adding file failed!\n"


                else:
                    print "KO, ack parsing failed\n"
                    print "Download not available"
    # end of download method



    def logout(self):

        """
        this method allows user to logout from P2P network
        """
        print "Logout...\n"

        self.dir_socket.send("LOGO" + self.session_ID) #invio la stringa di logout alla directory

        # Acknowledge "ALGO" dalla directory
        ack = self.dir_socket.recv(7)
        print ack

        if ack[:4]=="ALGO":

            print "OK, ack received\n"
            num_delete = ack[4:7]
            print "Number of deleted files: " + num_delete + "\n"


            if int(num_delete) != len(self.fileTable) :
                print "Warning: The number of copies deleted differs from those uploaded \n"

            self.dir_socket.close() #chiudo la socket verso la directory

            #inoltre devo smettere di ascoltare su IP e porta del P2p

            self.logged=False #non sono piu' loggato

        else :
            print "KO, ack parsing failed\n"
            self.logged=True #sono ancora loggato
    # end of logout method




    def error(self):
        print "Option not valid: try again!\n"
    # end of error method



    def doYourStuff(self):

        """
        This methods allow user to navigate into menus
        """
        if self.logged==False:

            print "Do you want to do login? (Y/N)\n"

        else: #allora sono loggato

            print "Choose between the following options, typing the number:\n"

            print "1. Add file"
            print "2. Delete file"
            print "3. Find and Download file"
            print "4. Logout\n"

        choice = raw_input("Choose an option: ")

        optNoLog = {

            'Y' : self.login,
            'N' : self.nologin,
        }

        optLog = {

            '1' : self.addfile,
            '2' : self.delfile,
            '3' : self.find,
            '4' : self.logout

        }

        print

        if self.logged==False: #non sono loggato

            optNoLog.get(choice,self.error)() #se l'utente ha digitato un qualcosa che non esiste, viene chiamata error()

        else: #sono loggato

            optLog.get(choice,self.error)() #se l'utente ha digitato un qualcosa che non esiste, viene chiamata error()
    # end of doYourStuff method



if __name__ == "__main__":

    nc = NapsterClient() #inizializzazione


    while nc.stop==False:

        nc.doYourStuff() #stampa del menu ed esecuzione dell'operazione scelta