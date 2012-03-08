__author__ = 'ingiulio maury puccigui'
import socket
from socket import *

host = "0.0.0.0" #mettere quello della directory
port = 9999
addr = host, port
P2P_port = 6500

while 1:

    print "Choose between the following options, typing the number:\n"
    print "1. Login"
    print "2. Add file"
    print "3. Delete file"
    print "4. Logout"
    print "5. Find"
    print "6. Download\n"

    data = raw_input("Choose an option: ")

    def login():

        print "Login...\n"
        dir = socket(AF_INET, SOCK_STREAM)
        dir.connect(addr)
        print "Connection with directory enstablished"
        my_IP = dir.getsockname()[0]

        print "My IP: " + my_IP
        my_IP_split = my_IP.split(".")
        IP_1 = '%(#)03d' % {"#" : int(my_IP_split[0])}
        IP_2 = '%(#)03d' % {"#" : int(my_IP_split[1])}
        IP_3 = '%(#)03d' % {"#" : int(my_IP_split[2])}
        IP_4 = '%(#)03d' % {"#" : int(my_IP_split[3])}
        IPP2P = IP_1 + "." + IP_2 + "." + IP_3 + "." + IP_4

        my_port = str(dir.getsockname()[1])
        print "My port: " + my_port
        PP2P = '%(#)05d' % {"#" : int(P2P_port)}

        dir.send("LOGI" + IPP2P + PP2P)

        # acknowledge
        ack = dir.recv(20)
        print ack

        if ack[:4]=="ALOG": #se non funziona ALOG usare ALGI
            print "OK, ack received\n"
            session_ID = ack[4:20]
            print "Session ID: " + session_ID + "\n"
	    # server socket creation
	    peersocket = socket(AF_INET, SOCK_STREAM)
	    peersocket.bind(my_IP,PP2P)
	    peersocket.listen(100)
        else :
            print "KO, ack parsing failed\n"

        if ack[4:20]=="0000000000000000":
            print "Login failed: try again!"
            dir.close()



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

print "\nFine."
