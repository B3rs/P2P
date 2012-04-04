#
# UI (and later GUI) settings and operations are to be implemented here
#
__author__ = 'LucaFerrari MarcoBersani GiovanniLodi'

from threading import Thread
import sys

class UIThread(Thread):

    def run(self):
        #print "UI thread started"

        while 1:
            print "Press 1 to search a file in the network"
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