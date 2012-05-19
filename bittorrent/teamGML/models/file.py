__author__ = 'LucaFerrari MarcoBersani GiovanniLodi'

import os, math
from models.partsmask import PartsMask
from models.peer import Peer

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

    def parts_mask_for_peer(self, peer):
        if self.parts_masks.has_key( str(peer)):
            part_mask = self.parts_masks[str(peer)]
            return part_mask
        else:
            raise Exception("Peer %s, does not have %s" %(str(peer), self.filename))

    def peer_has_part(self, peer, part_num):
        parts_mask = self.parts_mask_for_peer(peer)
        return parts_mask.is_available(part_num)

    def set_peer_has_part(self, peer, part_num, has_part):
        if not self.parts_masks.has_key( str(peer)):
            self.parts_masks[str(peer)] = PartsMask(self.parts_count)

        self.parts_masks[str(peer)].set_available(part_num, has_part)


    def get_peers_for_file_part(self, part_num):
        peers = []

        for (peer, part_mask) in self.parts_masks:
            if part_mask.is_available(part_num):
                peers.append(peer)

        return peers

    def is_local(self):
        return len(self.filepath)>0

    def set_peer_status_for_part(self, peer, part_num, status):
        if not self.parts_masks.has_key(str(peer)):
            self.parts_masks[str(peer)] = PartsMask(self.parts_count)

        self.parts_masks[str(peer)].set_part_status(part_num, status)

    def is_completed(self):
        local_peer = Peer.get_local_peer()

        for part_num in self.parts_count:
            if not self.peer_has_part(local_peer, part_num):
                return False
        return True