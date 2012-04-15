__author__ = 'LucaFerrari MarcoBersani GiovanniLodi'

from models.peer import Peer
from custom_utils.formatting import *

PEERS = [] #TODO: remove this into a singleton instance of PeersManager

class PeersManager(object):

    # @returns array with known peers
    @classmethod
    def find_known_peers(cls):
        return PEERS

    @classmethod
    def is_known_peer(cls, ip, port):
        for peer in PeersManager.find_known_peers():
            if PeersManager.are_same_peer(peer, Peer(ip, port)):
                return True
        return False

    @classmethod
    def are_same_peer(cls, peer1, peer2):
        return peer1.ip == peer2.ip and peer1.port == peer2.port

    # @returns add a new known
    @classmethod
    def add_new_peer(cls, peer_ip, peer_port):
        if not PeersManager.is_known_peer(peer_ip, peer_port):
            PEERS.append(Peer(peer_ip, peer_port))
