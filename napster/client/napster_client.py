__author__ = 'ingiulio'

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


    def md5_for_file(self,fileName): #gli passo il nome (o percorso) di un file

        print "funzione che calcola l'md5 di un file"

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
        self.dir_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket verso la directory
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
        self.IPP2P = IP_1 + "." + IP_2 + "." + IP_3 + "." + IP_4 #IP formattato per bene

        # Formattazione porta
        my_port = str(self.dir_socket.getsockname()[1]) #porta non ancora formattata
        print "My port: " + my_port
        self.PP2P = '%(#)05d' % {"#" : int(self.P2P_port)} #porta formattata per bene

        # SPEDISCO IL PRIMO MESSAGGIO
        self.dir_socket.send("LOGI" + self.IPP2P + self.PP2P)

        # Acknowledge "ALGI" dalla directory
        ack = self.dir_socket.recv(20)
        print ack

        if ack[:4]=="ALGI": # se non funziona ALGI usare ALOG

            print "OK, ack received\n"
            self.session_ID = ack[4:20]
            print "Session ID: " + self.session_ID + "\n"
            self.logged=True #sono loggato

            # Check login non riuscito
            if self.session_ID=="0000000000000000":
                print "Login failed: try again!"
                self.dir_socket.close()
                self.logged=False #non sono loggato

            # server socket creation
            #peersocket = serversocket.socket(serversocket.AF_INET, serversocket.SOCK_STREAM)
            #peersocket.bind(my_IP,PP2P) #bisognerebbe controllare che per sfiga non sia la stessa che mi porta alla directory
            #peersocket.listen(100)


        else :
            print "KO, ack parsing failed\n"
            self.logged=False #non sono loggato



    def nologin(self):
        print "You're about to exit the program... Bye!\n"
        self.stop = True




    def addfile(self):
        print "Add file...\n"

        nc.md5_for_file("PIPPO.jpeg")









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
            print "4. Download\n"
            print "5. Logout\n"

        data = raw_input("Choose an option: ")

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

            optNoLog.get(data,self.error)() #se l'utente ha digitato un qualcosa che non esiste, viene chiamata error()

        else: #sono loggato

            optLog.get(data,self.error)() #se l'utente ha digitato un qualcosa che non esiste, viene chiamata error()




if __name__ == "__main__":

    nc = NapsterClient() #inizializzazione


    while nc.stop==False:

        nc.doYourStuff() #stampa del menu ed esecuzione dell'operazione scelta

    print "Fine\n"