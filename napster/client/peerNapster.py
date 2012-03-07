__author__ = 'ingiulio maury puccigui'
import socket
from socket import *

host = "10.42.43.1" #da mettere quello di luca
port = 800 #giusta?
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

        print "Sto per fare: login\n"
        dir = socket(AF_INET, SOCK_STREAM) #creo la socket lato client #ho rinominato la socket (adesso si chiama dir come directory)
        print "ho fatto dir = socket()"
        dir.connect(addr) #mi connetto alla directory centralizzata
        print "Connessione con il Server stabilita"
        my_IP = dir.getsockname()[0]

        print "mio IP: " + my_IP
        my_IP_split = my_IP.split(".")
        IP_1 = '%(#)03d' % {"#" : int(my_IP_split[0])}
        IP_2 = '%(#)03d' % {"#" : int(my_IP_split[1])}
        IP_3 = '%(#)03d' % {"#" : int(my_IP_split[2])}
        IP_4 = '%(#)03d' % {"#" : int(my_IP_split[3])}
        IP_tot = IP_1 + "." + IP_2 + "." + IP_3 + "." + IP_4


        my_port = str(dir.getsockname()[1])
        print "mia porta: " + my_port
        PORT = '%(#)05d' % {"#" : int(my_port)}

        dir.send("LOGI." + IP_tot + "." + PORT) #mando alla directory la stringa di login

        ack = dir.recv(21)
        print ack

        if ack[:4]=="ALOG":
            print "ok, ack ricevuto\n"
            session_ID = ack[5:21]
            print "session ID: " + session_ID + "\n"
        else :
            print "ko, ack errato\n"



    def addfile():
        print "Sto per fare: aggiunta file\n"

    def delfile():
        print "Sto per fare: rimozione file\n"

    def logout():
        print "Sto per fare: logout\n"

    def find():
        print "Sto per fare: ricerca file\n"

    def download():
        print "Sto per fare: download file\n"

    def error():
        print "Errore! Scegli bene!\n"

    options = {
        '1' : login,
        '2' : addfile,
        '3' : delfile,
        '4' : logout,
        '5' : find,
        '6' : download
    }

    print 

    options.get(data,error)() #esegue la funzione che l'utente ha specificato
                                #se l'utente ha digitato un qualcosa che non esiste, viene chiamata error()

print "\nFine."
