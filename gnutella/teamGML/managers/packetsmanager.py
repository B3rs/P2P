__author__ = 'LucaFerrari MarcoBersani GiovanniLodi'

from models.packet import Packet

PACKETS = [] #TODO: remove this into a singleton instance of PeersManager

class PacketsManager(object):

    # @returns array with known peers
    @classmethod
    def get_packets(cls):
        return PACKETS

    # @returns true if the packet is already in the list
    @classmethod
    def is_packet_known(cls, packet):
        for p in PACKETS:
            if p.id == packet.id:
                return true
        return false

    # @returns true if the packet is already in the list
    @classmethod
    def is_packet_id_known(cls, packet_id):
        for p in PACKETS:
            if p.id == packet_id:
                return True
        return False

    # @returns add a new known
    @classmethod
    def add_new_packet(cls, packet_id, packet_sender = None):
        if not PacketsManager.is_packet_id_known(packet_id):
            packet = Packet(packet_id, packet_sender)
            PACKETS.append(packet)
