__author__ = 'ingiulio'
import socket
import serversocket
global session_ID #TODO verify

class NapsterClient(object):

    def __init__(self):

        print "Init Napster client"

        # DIRECTORY
        self.host = "192.168.0.194" # indirizzo della directory
        self.port = 800 # porta di connessione alla directory - DA SPECIFICHE: sarebbe la 80
        self.addr = host, port

        # PEER
        self.P2P_port = 6500 # porta che rendo disponibile per altri peer

    # USER HANDLERS

    def login(self): # secondo me va messo self. davanti a tutte le variabili che voglio rendere "condivise" tra tutti i metodi

        print "Login...\n"
        self.dir = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.dir.connect(self.addr)
        print "Connection with directory enstablished"

        # Formattazione indirizzo IP per invio alla directory
        my_IP = dir.getsockname()[0]
        print "My IP: " + my_IP
        my_IP_split = my_IP.split(".")
        IP_1 = '%(#)03d' % {"#" : int(my_IP_split[0])}
        IP_2 = '%(#)03d' % {"#" : int(my_IP_split[1])}
        IP_3 = '%(#)03d' % {"#" : int(my_IP_split[2])}
        IP_4 = '%(#)03d' % {"#" : int(my_IP_split[3])}
        self.IPP2P = IP_1 + "." + IP_2 + "." + IP_3 + "." + IP_4

        # Formattazione porta
        my_port = str(dir.getsockname()[1])
        print "My port: " + my_port
        self.PP2P = '%(#)05d' % {"#" : int(self.P2P_port)}

        # SPEDISCO IL PRIMO MESSAGGIO
        dir.send("LOGI" + self.IPP2P + self.PP2P)

        # Acknowledge "ALGI" dalla directory
        ack = dir.recv(20)
        print ack

        if ack[:4]=="ALGI": # se non funziona ALGI usare ALOG

            print "OK, ack received\n"
            self.session_ID = ack[4:20] # variabile globale
            print "Session ID: " + self.session_ID + "\n"

            # Check login non riuscito
            if self.session_ID=="0000000000000000":
                print "Login failed: try again!"
                self.dir.close()

            # server socket creation
            #peersocket = serversocket.socket(serversocket.AF_INET, serversocket.SOCK_STREAM)
            #peersocket.bind(my_IP,PP2P)
            #peersocket.listen(100)



        else :

            print "KO, ack parsing failed\n"


    def addfile():
        print "Add file...\n"

    def delfile():
        print "Delete file...\n"

    def logout():
        print "Logout...\n"

    def find():
        print "Find...\n"

    def download():
        print "Download...\n"

    def error():
        print "Option not valid: try again!\n"


    def doyourstuff(self):

        print "Choose between the following options, typing the number:\n"
        print "1. Login"
        print "2. Add file"
        print "3. Delete file"
        print "4. Logout"
        print "5. Find"
        print "6. Download\n"

        data = raw_input("Choose an option: ")

        options = {

            '1' : login,
            '2' : addfile,
            '3' : delfile,
            '4' : logout,
            '5' : find,
            '6' : download
        }

        print

        options.get(data,error)() #se l'utente ha digitato un qualcosa che non esiste, viene chiamata error()


if __name__ == "__main__":
    # 1. inizializzo
    nc = NapsterClient()
    while (1):
        # 2. stampo il menu
        nc.doyourstuff()
        print "ho finito di fare la tua roba"
    print "fine"