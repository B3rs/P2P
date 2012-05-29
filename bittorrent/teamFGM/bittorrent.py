__author__ = 'GuiducciGrillandaLoPiccolo'

import bittorrent_dir

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

        self.dir_port = 8000 # porta per i servizi di directory dei superpeer
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


    def exit(self):
        """
        exit method stop the program execution
        """
        print "You're about to exit the program"
        print "Bye!\n"
        self.stop = True
        # end of exit method


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
        #ricevo ALGI
        ack = self.sockread(super_sock,20)
        self.session_ID_1 = ack[4:20]
        self.closeConn(super_sock)

        #invio LOGI
        super_sock = self.openConn(self.my_IP, self.dir_port)
        super_sock.sendall("LOGI" + self.my_IP_form + "08888")
        #ricevo ALGI
        ack = self.sockread(super_sock,20)
        self.session_ID_2 = ack[4:20]
        self.closeConn(super_sock)

        """
        #invio LOGI
        super_sock = self.openConn(self.my_IP, self.dir_port)
        super_sock.sendall("LOGI" + self.my_IP_form + "07777")
        #ricevo ALGI
        ack = self.sockread(super_sock,20)
        self.session_ID_3 = ack[4:20]
        self.closeConn(super_sock)

        print "INIZIO AGGIUNTA FILE"
        """
        #invio ADDR
        super_sock = self.openConn(self.my_IP, self.dir_port)
        super_sock.sendall("ADDR" + self.session_ID_1 + "0101010101010101" + "0000819200" + "262144" + "                                                                                           pippo.txt")
        #ricevo AADR
        ack = self.sockread(super_sock,12)
        self.closeConn(super_sock)
        """
        #invio ADDR
        super_sock = self.openConn(self.my_IP, self.dir_port)
        super_sock.sendall("ADDR" + self.session_ID_2 + "0202020202020202" + "0000000176" + "000025" + "                                                                                           marco.txt")
        #ricevo AADR
        ack = self.sockread(super_sock,12)
        self.closeConn(super_sock)

        print "INIZIO RICERCA"

        #invio LOOK
        super_sock = self.openConn(self.my_IP, self.dir_port)
        super_sock.sendall("LOOK" + self.session_ID_2 + "                 pip")
        #ricevo ALOO
        ack = self.sockread(super_sock,7)
        numidrnd = int(ack[4:7])
        for i in range(0,numidrnd):
            ack = self.sockread(super_sock,132)
            print "file " + ack
        self.closeConn(super_sock)

        #invio LOOK
        super_sock = self.openConn(self.my_IP, self.dir_port)
        super_sock.sendall("LOOK" + self.session_ID_3 + "                   .")
        #ricevo ALOO
        ack = self.sockread(super_sock,7)
        numidrnd = int(ack[4:7])
        for i in range(0,numidrnd):
            ack = self.sockread(super_sock,132)
            print "file " + ack
        self.closeConn(super_sock)

        print "INIZIO FETCH"

        #invio FCHU
        super_sock = self.openConn(self.my_IP, self.dir_port)
        super_sock.sendall("FCHU" + self.session_ID_2 + "0101010101010101")
        #ricevo AFCH
        ack = self.sockread(super_sock,7)
        numhitpeer = int(ack[4:7])
        for i in range(0,numhitpeer):
            ack = self.sockread(super_sock,20)
            print "peer " + ack
            ack = self.sockread(super_sock,1) #TODO questo 1 in realta' dovrebbe essere il numero di byte da leggere
            print "partlist " + ack
        self.closeConn(super_sock)

        #invio FCHU
        super_sock = self.openConn(self.my_IP, self.dir_port)
        super_sock.sendall("FCHU" + self.session_ID_2 + "0202020202020202")
        #ricevo AFCH
        ack = self.sockread(super_sock,7)
        numhitpeer = int(ack[4:7])
        for i in range(0,numhitpeer):
            ack = self.sockread(super_sock,20)
            print "peer " + ack
            ack = self.sockread(super_sock,1) #TODO questo 1 in realta' dovrebbe essere il numero di byte da leggere
            print "partlist " + ack
        self.closeConn(super_sock)

        print "INIZIO AGGIUNTA PARTI"

        """

        #invio RPAD
        super_sock = self.openConn(self.my_IP, self.dir_port)
        super_sock.sendall("RPAD" + self.session_ID_2 + "0101010101010101" + "00000001")
        #ricevo APAD
        ack = self.sockread(super_sock,12)
        self.closeConn(super_sock)

        #invio RPAD
        super_sock = self.openConn(self.my_IP, self.dir_port)
        super_sock.sendall("RPAD" + self.session_ID_2 + "0101010101010101" + "00000002")
        #ricevo APAD
        ack = self.sockread(super_sock,12)
        self.closeConn(super_sock)

        #invio RPAD
        super_sock = self.openConn(self.my_IP, self.dir_port)
        super_sock.sendall("RPAD" + self.session_ID_2 + "0101010101010101" + "00000003")
        #ricevo APAD
        ack = self.sockread(super_sock,12)
        self.closeConn(super_sock)

        #invio RPAD
        super_sock = self.openConn(self.my_IP, self.dir_port)
        super_sock.sendall("RPAD" + self.session_ID_2 + "0101010101010101" + "00000004")
        #ricevo APAD
        ack = self.sockread(super_sock,12)
        self.closeConn(super_sock)

        """

        #invio RPAD
        super_sock = self.openConn(self.my_IP, self.dir_port)
        super_sock.sendall("RPAD" + self.session_ID_3 + "0101010101010101" + "00000002")
        #ricevo APAD
        ack = self.sockread(super_sock,12)
        self.closeConn(super_sock)

        #invio RPAD
        super_sock = self.openConn(self.my_IP, self.dir_port)
        super_sock.sendall("RPAD" + self.session_ID_3 + "0101010101010101" + "00000003")
        #ricevo APAD
        ack = self.sockread(super_sock,12)
        self.closeConn(super_sock)

        #invio RPAD
        super_sock = self.openConn(self.my_IP, self.dir_port)
        super_sock.sendall("RPAD" + self.session_ID_3 + "0101010101010101" + "00000004")
        #ricevo APAD
        ack = self.sockread(super_sock,12)
        self.closeConn(super_sock)

        #invio RPAD
        super_sock = self.openConn(self.my_IP, self.dir_port)
        super_sock.sendall("RPAD" + self.session_ID_3 + "0101010101010101" + "00000005")
        #ricevo APAD
        ack = self.sockread(super_sock,12)
        self.closeConn(super_sock)

        #invio RPAD
        super_sock = self.openConn(self.my_IP, self.dir_port)
        super_sock.sendall("RPAD" + self.session_ID_3 + "0202020202020202" + "00000001")
        #ricevo APAD
        ack = self.sockread(super_sock,12)
        self.closeConn(super_sock)

        #invio RPAD
        super_sock = self.openConn(self.my_IP, self.dir_port)
        super_sock.sendall("RPAD" + self.session_ID_3 + "0202020202020202" + "00000002")
        #ricevo APAD
        ack = self.sockread(super_sock,12)
        self.closeConn(super_sock)

        #invio RPAD
        super_sock = self.openConn(self.my_IP, self.dir_port)
        super_sock.sendall("RPAD" + self.session_ID_3 + "0202020202020202" + "00000003")
        #ricevo APAD
        ack = self.sockread(super_sock,12)
        self.closeConn(super_sock)

        #invio RPAD
        super_sock = self.openConn(self.my_IP, self.dir_port)
        super_sock.sendall("RPAD" + self.session_ID_3 + "0202020202020202" + "00000004")
        #ricevo APAD
        ack = self.sockread(super_sock,12)
        self.closeConn(super_sock)

        #invio RPAD
        super_sock = self.openConn(self.my_IP, self.dir_port)
        super_sock.sendall("RPAD" + self.session_ID_3 + "0202020202020202" + "00000005")
        #ricevo APAD
        ack = self.sockread(super_sock,12)
        self.closeConn(super_sock)

        #invio RPAD
        super_sock = self.openConn(self.my_IP, self.dir_port)
        super_sock.sendall("RPAD" + self.session_ID_3 + "0202020202020202" + "00000005")
        #ricevo APAD
        ack = self.sockread(super_sock,12)
        self.closeConn(super_sock)

        print "INIZIO LOGOUT"

        #invio LOGO
        super_sock = self.openConn(self.my_IP, self.dir_port)
        super_sock.sendall("LOGO" + self.session_ID_1)
        #ricevo ALGO
        ack = self.sockread(super_sock,14)
        self.closeConn(super_sock)

        #invio LOGO
        super_sock = self.openConn(self.my_IP, self.dir_port)
        super_sock.sendall("LOGO" + self.session_ID_2)
        #ricevo ALGO
        ack = self.sockread(super_sock,14)
        self.closeConn(super_sock)

        #invio LOGO
        super_sock = self.openConn(self.my_IP, self.dir_port)
        super_sock.sendall("LOGO" + self.session_ID_3)
        #ricevo ALGO
        ack = self.sockread(super_sock,14)
        self.closeConn(super_sock)
        """


        choice = ""
        while choice != "Y":
            choice = raw_input("If you want to logout press Y: ")

            if choice == "Y":
                self.exit()
            else:
                print "Option not valid: try again!\n"


        # end of doYourStuff method



if __name__ == "__main__":

    bc = BittorrentClient() #inizializzazione


    while bc.stop==False:

        bc.doYourStuff() #stampa del menu ed esecuzione dell'opera

    sys.exit()