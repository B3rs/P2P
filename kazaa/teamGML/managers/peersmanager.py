__author__ = 'LucaFerrari MarcoBersani GiovanniLodi'

from models.peer import Peer
from custom_utils.formatting import *

PEERS = [] #TODO: remove this into a singleton instance of PeersManager

class PeersManager(object):

    # @returns array with known peers
    @classmethod
    def find_known_peers(cls, superpeers=False):
        if superpeers:
            matching = []
            for p in PEERS:
                if p.is_superpeer:
                    matching.append(p)
            return matching
        else:
            return PEERS

    @classmethod
    def is_known_peer(cls, peer):
        for peer2 in PeersManager.find_known_peers():
            if PeersManager.are_same_peer(peer, peer2):
                return True
        return False

    @classmethod
    def are_same_peer(cls, peer1, peer2):
        return peer1.ip == peer2.ip and peer1.port == peer2.port

    # @returns add a new known
    @classmethod
    def add_new_peer(cls, peer):
        if not PeersManager.is_known_peer(peer):
            PEERS.append(peer)
