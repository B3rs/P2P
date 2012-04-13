__author__ = 'LucaFerrari MarcoBersani GiovanniLodi'

from models.packet import Packet
import time

#TODO: remove this into a singleton instance of PeersManager
PACKETS = []
GENERATED_PACKETS = []

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

    # @returns array with known peers
    @classmethod
    def get_generated_packets(cls):
        return GENERATED_PACKETS

    # @returns true if the packet is already in the list
    @classmethod
    def is_generated_packet_id_known(cls, packet_id):
        for p in GENERATED_PACKETS:
            if p.id == packet_id:
                return True
        return False

    # @returns add a new known
    @classmethod
    def add_new_generated_packet(cls, packet_id, packet_sender = None):
        if not PacketsManager.is_generated_packet_id_known(packet_id):
            packet = Packet(packet_id, packet_sender)
            GENERATED_PACKETS.append(packet)

    @classmethod
    def get_generated_packet_by_id(cls, packet_id):
        for p in GENERATED_PACKETS:
            if p.id == packet_id:
                return p
        return None

    @classmethod
    def is_generated_packet_still_valid(cls, packet_id):
        if PacketsManager.is_generated_packet_id_known(packet_id):
            delta = time.time() - PacketsManager.get_generated_packet_by_id(packet_id).timestamp
            print delta
            if delta <= 300:
                return True
        return False
