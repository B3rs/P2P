__author__ = 'LucaFerrari MarcoBersani GiovanniLodi'

import os, math
from models.partsmask import PartsMask

DEFAULT_PART_SIZE = 262144 #numero dei bit

class File(object):
    def __init__(self, id, name, path=''):
        self.filepath = path
        self.filename = name
        self.id = id
        self.file_size = -1
        self.part_size = -1
        self.parts_count = -1
        self.parts_masks = {} #{ 'idPeer': partsMask, 'idPeer': partsMask}

        if len(path) > 0:
            self.file_size = os.path.getsize(path)

            if self.file_size > DEFAULT_PART_SIZE:
                self.part_size = 256
            else:
                self.part_size = self.file_size

            self.parts_count = math.ceil(self.file_size / self.part_size)


    def peer_has_part(self, peer, part_num):
        if self.parts_masks.has_key( str(peer)):
            part_mask = self.parts_masks[str(peer)]
            return part_mask.is_available(part_num)
        else:
            raise Exception("Peer %s, does not have %s" %(str(peer), self.filename))

    def set_peer_has_part(self, peer, part_num):
        if not self.parts_masks.has_key( str(peer)):
            self.parts_masks[str(peer)] = PartsMask(self.parts_count)

        self.parts_masks[str(peer)].set_available(part_num)

    def get_peers_for_file_part(self, part_num):
        peers = []

        for (peer, part_mask) in self.parts_masks:
            if part_mask.is_available(part_num):
                peers.append(peer)

        return peers

    def is_local(self):
        return len(self.filepath)>0