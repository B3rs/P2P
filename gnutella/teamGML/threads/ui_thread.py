#
# UI (and later GUI) settings and operations are to be implemented here
#
__author__ = 'LucaFerrari MarcoBersani GiovanniLodi'

from threading import Thread
from models.peer import Peer
import sys

class UIThread(Thread):

    def __init__(self, known_peers):
        super(UIThread, self).__init__()
        self.known_peers = known_peers

    def run(self):
        #print "UI thread started"

        print "You now need to insert your known peers\n"
        ip = raw_input("Please insert a known peer ip ")
        port = raw_input("and now please insert its port ")
        p = Peer(ip, port)
        self.known_peers.append(p)

        while raw_input("Do you know other peers? (y/n) ") != 'n':
            ip = raw_input("Please insert a known peer ip ")
            port = raw_input("and now please insert its port ")
            p = Peer(ip, port)
            self.known_peers.append(p)

        print "Your known peers are\n"
        for peer in self.known_peers:
            print "\t" + peer.ip + ":" + peer.port # Doesn't work :(

        while 1:
            print "\nPress 1 to search a file in the network"
            print "Press 2 to update the known peer list"

            cmd = raw_input()

            if cmd == "1":
                print "U pressed 1 :)\n"
                pass
            elif cmd == "2":
                print "U pressed 2 :)\n"
                pass
            else:
                print "Invalid command! %s" %cmd