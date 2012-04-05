__author__ = 'LucaFerrari MarcoBersani GiovanniLodi'

from models.peer import Peer

class PeersManager(object):

    # @returns array with known peers
    @classmethod
    def find_known_peers(cls):
        peers = []
        for i in xrange(5):
            peers.append(Peer("192.168.1.10%d" % i, 80))
        return peers
