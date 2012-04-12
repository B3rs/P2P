__author__ = 'LucaFerrari MarcoBersani GiovanniLodi'

import socket
from threading import Thread
from models.peer import Peer
from managers.peersmanager import PeersManager
from custom_utils.formatting import *
from custom_utils.hashing import generate_packet_id

#TODO: where is the run method????????
class RequestEmitterThread(Thread):

    def __init__(self, local_port):
        super(RequestEmitterThread, self).__init__()
        self.local_port = local_port

    def search_for_peers(self):
        print "Started query flooding for peers" # TODO write better
        for peer in PeersManager.find_known_peers():
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # useful to avoid boring address already in use
            sock.connect((peer.ip, peer.port))
            local_ip = sock.getsockname()[0]
            p_id = generate_packet_id(16) #TODO: generate
            ttl = 3
            sock.send("NEAR" + p_id + format_ip_address(local_ip) + format_port_number(self.local_port) + str(ttl))
            sock.close()

    def search_for_files(self, query):
        print "Started query flooding for files: %s" %query
        print "TODO"

    def download_file(self, peer_ip, peer_port, md5):
        print "Download....."
        print "TODO"