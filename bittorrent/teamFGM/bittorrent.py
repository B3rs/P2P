__author__ = 'GuiducciGrillandaLoPiccolo'

import bittorrent_dir
import bittorrent_dir_serv

import sys
import socket #TOGLIERE DOPO DEBUG

class BittorrentClient(object):

    def __init__(self):

        """
        This method set the program parameters, such as IPP2P:P2P to allow others connection from/to other peers
        and IP address of Centralized Directory
        """

        # PEER

        #OS X
        #self.my_IP = socket.gethostbyname(socket.gethostname())

        #Linux
        self.my_IP = "192.168.0.103"

        my_IP_split = self.my_IP.split(".")
        IP_1 = '%(#)03d' % {"#" : int(my_IP_split[0])}
        IP_2 = '%(#)03d' % {"#" : int(my_IP_split[1])}
        IP_3 = '%(#)03d' % {"#" : int(my_IP_split[2])}
        IP_4 = '%(#)03d' % {"#" : int(my_IP_split[3])}
        self.my_IP_form = IP_1 + "." + IP_2 + "." + IP_3 + "." + IP_4 #IP formattato per bene

        self.dir_port = 80 # porta per i servizi di directory dei superpeer
        self.dir_port_form = '%(#)05d' % {"#" : int(self.dir_port)} #porta formattata per bene

        self.stop = False #non voglio uscire subito dal programma

        print ""

        # end of __init__ method


    # Definition of auxiliary methods

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


    def printpeers(self):

        print ""

    def printfiles(self):

        print ""


    def exit(self):
        """
        exit method stop the program execution
        """
        print "You're about to exit the program"
        print "Bye!\n"
        self.stop = True
        # end of exit method


    def error(self):
        print "Option not valid: try again!\n"
        # end of error method


    def openConn(self, IP, port): #DA TOGLIERE DOPO DEBUG
        #mi connetto al vicino
        neigh_addr = (IP, int(port))
        try:
            #print "Connecting with Neighbour " + IP
            neigh_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            neigh_socket.connect(neigh_addr)
        except IOError, expt: #IOError exception includes a sub-exception socket.error
            print "Error occured in Connection with neighbour -> %s" % expt + "\n"
        else:
            return neigh_socket
            # end of method openConn


    def closeConn(self, socket): #DA TOGLIERE DOPO DEBUG
        #mi disconnetto dal vicino
        try:
            socket.close()
        except IOError, expt: #IOError exception includes a sub-exception socket.error
            print "Error occured in Disconnection with neighbour -> %s" % expt + "\n"
            # end of method closeConn


    def doYourStuff(self):

        """
        This methods allow user to navigate into menu and logging in
        """

        self.mydirectory = bittorrent_dir.ListenToPeers(self.my_IP_form, self.dir_port_form) #mio indirizzo, porta 80
        self.mydirectory.start()

        print "You're listening on address " + self.my_IP + " port " + str(self.dir_port) + "\n"


        #PROVE DI DEBUG IN CUI SIMULO DI ESSERE UN CLIENT

        #invio LOGI
        super_sock = self.openConn(self.my_IP, self.dir_port)
        super_sock.sendall("LOGI" + self.my_IP_form + "09999")
        print "sent LOGI" + self.my_IP_form + "09999" + " to " + self.my_IP + ":" + str(self.dir_port)
        #ricevo ALGI
        ack = self.sockread(super_sock,20)
        print "received " + ack
        self.session_ID = ack[4:20]
        #invio LOGO
        super_sock = self.openConn(self.my_IP, self.dir_port)
        super_sock.sendall("LOGO" + self.session_ID)
        print "sent LOGO" + self.session_ID + " to " + self.my_IP + ":" + str(self.dir_port)
        #ricevo ALGO
        ack = self.sockread(super_sock,14)
        print "received " + ack



        print "Choose between the following options, typing the number:\n"

        print "1. Print peers" #potrebbe essere un'idea carina
        print "2. Print files" #potrebbe essere un'idea carina
        print "3. Exit\n"

        choice = raw_input("Choose an option: ")

        opt = {

            '1' : self.printpeers,
            '2' : self.printfiles,
            '3' : self.exit,

        }

        print ""

        opt.get(choice,self.error)() #se l'utente ha digitato un qualcosa che non esiste, viene chiamata error()

        # end of doYourStuff method



if __name__ == "__main__":

    bc = BittorrentClient() #inizializzazione


    while bc.stop==False:

        bc.doYourStuff() #stampa del menu ed esecuzione dell'opera

    sys.exit()