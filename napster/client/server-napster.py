### server

from socket import *
host = "192.168.0.194"
port = 800

test = socket(AF_INET, SOCK_STREAM)
test.bind((host, port))
test.listen(5) # definisce il numero max di connessioni simultanee
print "Server connesso"
conn, addr = test.accept() #la funzione accept() mette il socket in listening
print "Indirizzo socket", conn
print "Server contattato da", addr

i=0

while i<5:
    data = conn.recv(1024)
    print data
    i=i+1

test.close()
print "\nFine."
