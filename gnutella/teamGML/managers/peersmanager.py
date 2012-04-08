__author__ = 'LucaFerrari MarcoBersani GiovanniLodi'

from models.peer import Peer

PEERS = [] #TODO: remove this into a singleton instance of PeersManager

class PeersManager(object):

    # @returns array with known peers
    @classmethod
    def find_known_peers(cls):
        return PEERS

    # @returns add a new known
    @classmethod
    def add_new_peer(cls, peer_ip, peer_port):
        peer = Peer(peer_ip, peer_port)
        PEERS.append(peer)
