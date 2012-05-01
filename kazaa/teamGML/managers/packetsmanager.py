__author__ = 'LucaFerrari MarcoBersani GiovanniLodi'

from models.packet import Packet
import time
from custom_utils.logging import *

TIME_THRESHOLD = 20#300


class PacketsManager(object):

    PACKETS = []
    GENERATED_PACKETS = []
    # Will contain only the packet id, so that all the handling will fallback to the normal packets methods
    LOCAL_SEARCHES = []


    # @returns array with known peers
    @classmethod
    def get_packets(cls):
        return PacketsManager.PACKETS

    # @returns true if the packet is already in the list
    @classmethod
    def is_packet_known(cls, packet):
        for p in PacketsManager.PACKETS:
            if p.id == packet.id:
                return True
        return False

    # @returns true if the packet is already in the list
    @classmethod
    def is_packet_id_known(cls, packet_id):
        for p in PacketsManager.PACKETS:
            if p.id == packet_id:
                return True
        return False

    # @returns add a new known
    @classmethod
    def add_new_packet(cls, packet_id, packet_sender = None):
        if not PacketsManager.is_packet_id_known(packet_id):
            packet = Packet(packet_id, packet_sender)
            PacketsManager.PACKETS.append(packet)

    # @returns array with known peers
    @classmethod
    def get_generated_packets(cls):
        return PacketsManager.GENERATED_PACKETS

    # @returns true if the packet is already in the list
    @classmethod
    def is_generated_packet_id_known(cls, packet_id):
        for p in PacketsManager.GENERATED_PACKETS:
            if p.id == packet_id:
                return True
        return False

    # @returns add a new known
    @classmethod
    def add_new_generated_packet(cls, packet_id, packet_sender = None):
        if not PacketsManager.is_generated_packet_id_known(packet_id):
            packet = Packet(packet_id, packet_sender)
            PacketsManager.GENERATED_PACKETS.append(packet)

    @classmethod
    def get_generated_packet_by_id(cls, packet_id):
        for p in PacketsManager.GENERATED_PACKETS:
            if p.id == packet_id:
                return p
        return None

    @classmethod
    def is_generated_packet_still_valid(cls, packet_id):
        if PacketsManager.is_generated_packet_id_known(packet_id):
            delta = time.time() - PacketsManager.get_generated_packet_by_id(packet_id).timestamp
            print delta
            if delta <= TIME_THRESHOLD:
                return True
        return False

    #
    #   Method for the local search handling
    #
    @classmethod
    def register_packet_id_as_local_search(cls, packet_id):
        if PacketsManager.is_generated_packet_id_known(packet_id) and not PacketsManager.is_local_search(packet_id):
            PacketsManager.LOCAL_SEARCHES.append(packet_id)

    @classmethod
    def is_local_search(cls, packet_id):
        for id in PacketsManager.LOCAL_SEARCHES:
            if packet_id == id and PacketsManager.is_generated_packet_still_valid(packet_id):
                return True
        return False
