__author__ = 'ingiulio maury puccigui'
import socket
from socket import *

host = "10.42.43.1" #mettere quello della directory
port = 800
addr = host, port

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
        IP_tot = IP_1 + "." + IP_2 + "." + IP_3 + "." + IP_4


        my_port = str(dir.getsockname()[1])
        print "My porta: " + my_port
        PORT = '%(#)05d' % {"#" : int(my_port)}

        dir.send("LOGI" + IP_tot + PORT)

        # acknowledge
        ack = dir.recv(20)
        print ack

        if ack[:4]=="ALOG": #se non funziona ALOG usare ALGI
            print "OK, ack received\n"
            session_ID = ack[4:20]
            print "Session ID: " + session_ID + "\n"
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
