__author__ = 'LucaFerrari MarcoBersani GiovanniLodi'

from models.peer import Peer
from custom_utils.formatting import format_ip_address

PEERS = [] #TODO: remove this into a singleton instance of PeersManager

class PeersManager(object):

    # @returns array with known peers
    @classmethod
    def find_known_peers(cls):
        return PEERS

    @classmethod
    def is_known_peer(cls, ip):
        for peer in PEERS:
            if peer.ip == format_ip_address(ip):
                return True
        return False

    # @returns add a new known
    @classmethod
    def add_new_peer(cls, peer_ip, peer_port):
        peer = Peer(peer_ip, peer_port)
        if not PeersManager.is_known_peer(peer_ip):
            PEERS.append(peer)
