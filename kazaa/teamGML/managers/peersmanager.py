__author__ = 'LucaFerrari MarcoBersani GiovanniLodi'

from models.peer import Peer
from custom_utils.formatting import *


class PeersManager(object):

    PEERS = []

    # @returns array with known peers
    @classmethod
    def find_known_peers(cls, superpeers=False):
        if superpeers:
            matching = []
            for p in PeersManager.PEERS:
                if p.is_superpeer:
                    matching.append(p)
            return matching
        else:
            return PeersManager.PEERS

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
            PeersManager.PEERS.append(peer)

    @classmethod
    def become_superpeer(cls, ip, port):
        for p in PeersManager.PEERS:
            if p.ip == ip and p.port == port:
                p.is_superpeer = True
