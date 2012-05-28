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
                self.part_size = DEFAULT_PART_SIZE
            else:
                self.part_size = self.file_size

            self.calculate_parts_count()

    def calculate_parts_count(self):
        self.parts_count = int(math.ceil(self.file_size / self.part_size))

        if (self.file_size % self.part_size) != 0:
            self.parts_count +=1

        return

    def set_file_and_part_size(self, file_size, part_size):
        self.file_size = int(file_size)
        self.part_size = int(part_size)

        self.calculate_parts_count()


    def parts_mask_for_peer(self, peer):
        if not self.parts_masks.has_key( str(peer)):
             self.parts_masks[str(peer)] = PartsMask(self.parts_count)

        part_mask = self.parts_masks[str(peer)]
        return part_mask

    def peer_has_part(self, peer, part_num):
        parts_mask = self.parts_mask_for_peer(peer)
        return parts_mask.is_available(part_num)

    def set_peer_has_part(self, peer, part_num, has_part):
        if not self.parts_masks.has_key( str(peer)):
            self.parts_masks[str(peer)] = PartsMask(self.parts_count)

        self.parts_masks[str(peer)].set_available(part_num, has_part)


    def get_peers_for_file_part(self, part_num):
        peers = []

        for (peer_str, part_mask) in self.parts_masks.items():
            if part_mask.is_available(part_num):
                peers.append(Peer.peer_from_string(peer_str))

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

    def get_part_size(self, num):
        if num < self.parts_count - 1 and num >= 0:
            return self.part_size
        elif num == self.parts_count -1 :
            return os.path.getsize(self.filepath) - ((self.parts_count - 1) * self.part_size)

    def get_part(self, num):
        f = open(self.filepath, 'rb')
        f.seek(self.part_size * num)
        result = f.read(self.part_size)
        f.close()
        return result
