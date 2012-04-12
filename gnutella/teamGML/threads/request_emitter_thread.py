__author__ = 'LucaFerrari MarcoBersani GiovanniLodi'

import socket
from threading import Thread
from models.peer import Peer
from managers.peersmanager import PeersManager
from custom_utils.formatting import *
from custom_utils.hashing import generate_packet_id
from custom_utils.sockets import connect_socket

#TODO: where is the run method????????
class RequestEmitterThread(Thread):

    def __init__(self, local_port):
        super(RequestEmitterThread, self).__init__()
        self.local_port = local_port

    def search_for_peers(self):
        print "Started query flooding for peers" # TODO write better
        for peer in PeersManager.find_known_peers():
            sock = connect_socket(peer.ip, peer.port)
            local_ip = sock.getsockname()[0]
            p_id = generate_packet_id(16) #TODO: generate
            ttl = 3
            sock.send("NEAR" + p_id + format_ip_address(local_ip) + format_port_number(self.local_port) + str(ttl))
            sock.close()

    def search_for_files(self, query):
        print "Started query flooding for files: %s" %query
        for peer in PeersManager.find_known_peers():
            sock = connect_socket(peer.ip, peer.port)
            local_ip = sock.getsockname()[0]
            p_id = generate_packet_id(16) #TODO: generate
            ttl = 3
            sock.send("QUER" + p_id + format_ip_address(local_ip) + format_port_number(self.local_port) + str(ttl) + format_query(query))
            sock.close()

    def download_file(self, peer_ip, peer_port, md5):
        print "Download....."
        print "TODO"