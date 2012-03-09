__author__ = 'ingiulio'

from napster_client_threads import DownloadMe

import socket
#import serversocket
import hashlib #per calcolare l'md5 dei file

class NapsterClient(object):


    def __init__(self):

        print "Init Napster client\n"

        # DIRECTORY
        self.dir_host = "192.168.0.194" # indirizzo della directory
        self.dir_port = 800 # porta di connessione alla directory - DA SPECIFICHE: sarebbe la 80
        self.dir_addr = self.dir_host, self.dir_port

        # PEER
        self.P2P_port = 6500 # porta che rendo disponibile per altri peer quando vogliono fare download da me

        self.logged = False #non sono loggato
        self.stop = False #non voglio uscire subito dal programma


    def md5_for_file(self,fileName):

        print "Funzione che calcola l'md5 di un file"

        f = open(fileName)
        md5 = hashlib.md5()
        while True:
            data = f.read(128)
            if not data:
                break
            md5.update(data)
        print md5.digest()
        return md5.digest()


    # USER HANDLERS



    def login(self): # va messo self. davanti a tutte le variabili che voglio rendere "condivise" tra tutti i metodi

        print "Login...\n"

        #se sono riuscito senza problemi, mi connetto alla directory

        self.dir_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket verso la directory
        #aggiunge option by maury
        self.dir_socket.connect(self.dir_addr)
        print "Connection with directory enstablished"


        # Formattazione indirizzo IP per invio alla directory
        my_IP = self.dir_socket.getsockname()[0] #IP non ancora formattato
        print "My IP: " + my_IP
        my_IP_split = my_IP.split(".")
        IP_1 = '%(#)03d' % {"#" : int(my_IP_split[0])}
        IP_2 = '%(#)03d' % {"#" : int(my_IP_split[1])}
        IP_3 = '%(#)03d' % {"#" : int(my_IP_split[2])}
        IP_4 = '%(#)03d' % {"#" : int(my_IP_split[3])}
        self.IPP2P_form = IP_1 + "." + IP_2 + "." + IP_3 + "." + IP_4 #IP formattato per bene

        # Formattazione porta
        my_port = str(self.dir_socket.getsockname()[1]) #porta non ancora formattata
        print "My port: " + my_port #DEBUG
        self.PP2P_form = '%(#)05d' % {"#" : int(self.P2P_port)} #porta formattata per bene

        #metto a disposizione una porta per il peer to peer
        self.peersocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.peersocket.bind(my_IP,self.P2P_port)
        self.peersocket.listen(100) #socket per chi vorra' fare download da me

        # SPEDISCO IL PRIMO MESSAGGIO
        self.dir_socket.send("LOGI" + self.IPP2P_form + self.PP2P_form)

        # Acknowledge "ALGI" dalla directory
        ack = self.dir_socket.recv(20)
        print ack

        if ack[:4]=="ALGI": # se non funziona ALGI usare ALOG

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
                DownloadMe().start() #thread che gestisce il download da parte dei peer


        else :
            print "KO, ack parsing failed\n"
            self.logged=False #non sono loggato


    def nologin(self):
        print "You're about to exit the program... Bye!\n"
        self.stop = True



    def addfile(self):
        print "Add file...\n"

        filename = raw_input("Insert the file name: ")


        md5file = self.md5_for_file(filename) #calcolo l'md5 del file

        filename_100 = '%(#)0100s' % {"#" : filename} #formatto il nome del file

        print "filename formattato: " + filename_100

        # SPEDISCO IL MESSAGGIO
        self.dir_socket.send("ADDF" + self.session_ID + md5file + filename_100)

        # Acknowledge "AADD" dalla directory
        ack = self.dir_socket.recv(7)
        print ack

        if ack[:4]=="AADD":

            print "OK, ack received\n"
            num_copy = ack[4:7]
            print "Number of copies: " + num_copy + "\n"

            # Check num copies
            if int(num_copy) < 1:
                print "La directory non ha aggiunto il tuo file"
            else:
                print "Copia aggiunta!"


        else :
            print "KO, ack parsing failed\n"
            print "aggiunta file fallita!"





    def delfile(self):
        print "Delete file...\n"




    def find(self):
        print "Find...\n"




    def download(self):
        print "Download...\n"




    def logout(self):

        print "Logout...\n"

        self.dir_socket.send("LOGO" + self.session_ID) #invio la stringa di logout alla directory

        # Acknowledge "ALGO" dalla directory
        ack = self.dir_socket.recv(7)
        print ack

        if ack[:4]=="ALGO":

            print "OK, ack received\n"
            num_delete = ack[4:7]
            print "Number of deleted files: " + num_delete + "\n"

            self.dir_socket.close() #chiudo la socket verso la directory

            #inoltre devo smettere di ascoltare su IP e porta del P2p

            self.logged=False #non sono piu' loggato

        else :
            print "KO, ack parsing failed\n"
            self.logged=True #sono ancora loggato





    def error(self):
        print "Option not valid: try again!\n"



    def doYourStuff(self):

        if self.logged==False:

            print "Do you want to do login? (Y/N)\n"

        else: #ovvero se sono loggato

            print "Choose between the following options, typing the number:\n"

            print "1. Add file"
            print "2. Delete file"
            print "3. Find"
            print "4. Download"
            print "5. Logout\n"

        choice = raw_input("Choose an option: ")

        optNoLog = {

            'Y' : self.login,
            'N' : self.nologin,
        }

        optLog = {

            '1' : self.addfile,
            '2' : self.delfile,
            '3' : self.find,
            '4' : self.download,
            '5' : self.logout

        }

        print

        if self.logged==False: #non sono loggato

            optNoLog.get(choice,self.error)() #se l'utente ha digitato un qualcosa che non esiste, viene chiamata error()

        else: #sono loggato

            optLog.get(choice,self.error)() #se l'utente ha digitato un qualcosa che non esiste, viene chiamata error()




if __name__ == "__main__":

    nc = NapsterClient() #inizializzazione


    while nc.stop==False:

        nc.doYourStuff() #stampa del menu ed esecuzione dell'operazione scelta

    print "Fine\n"