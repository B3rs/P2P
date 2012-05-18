from custom_utils.logging import klog

__author__ = 'LucaFerrari MarcoBersani GiovanniLodi'
import os
from custom_utils import hashing
from models.file import File
from models.peer import Peer
from custom_utils.logging import klog



# TODO: WARNING!
# That way path is defined from this file location, but it doesn't work,
# because the method it's called form another file in a different location...
# TODO find a way to evaluate the path in a way that is transparent to the caller of the method
#SHARED_PATH = "../shared" # If u are a normal person
SHARED_PATH = "shared"  # If u are GIO
DOWNLOAD_FOLDER = "downloads"



class FilesManager(object):

    FILES = []

    @classmethod
    def get_files(cls):
        return FilesManager.FILES

    @classmethod
    def load_my_files(cls):
        peer_me = Peer.get_local_peer()
        for dirname, dirnames, filenames in os.walk(SHARED_PATH):
            for filename in filenames:
                path = dirname + "/" + filename
                file = File(hashing.generate_file_id(), filename,path)

                #Set that I have all this file
                for p in range(0, file.parts_count):
                    file.set_peer_has_part(peer_me, p)

                cls.get_files().append(file)

    @classmethod
    def delete_file(cls, file):
        cls.get_files().remove(file)

    @classmethod
    def find_file_by_id(cls, id):
        for file in cls.get_files():
            if file.id == id:
                return file
        return None

    @classmethod
    def shared_files(cls):
        results = []
        for f in cls.get_files():
            if f.is_local():
                results.append(f)
        return results

    @classmethod
    def add_new_remote_file(cls, file_name, file_id, file_size, part_size):
        file = File(file_id, file_name)
        file.file_size = file_size
        file.part_size = part_size
        cls.get_files().append(file)

    @classmethod
    def update_remote_file_part(cls, file_id, peer, part_num, available):
        file = cls.find_file_by_id(file_id)
        if file:
            file.set_peer_has_part(peer, part_num, available)
        else:
            raise Exception("File %s not found" %file_id)

    @classmethod
    def get_ordered_parts_number(cls, file_id):
        file = cls.find_file_by_id(file_id)
        if file:
            part_nums = []
            for p_num in range(0, file.parts_count):
                if not file.parts_mask_for_peer(Peer.get_local_peer()).is_not_started(p_num):
                    klog("TODO: ordinare gli indici delle parti da quella meno conosciuta a quella piu conosciuta")
                    part_nums.append(p_num)

            return part_nums
        else:
            raise Exception("File not found: %s" %file_id)

    @classmethod
    def get_completed_file_parts_count(cls, file_id):
        file = cls.find_file_by_id(file_id)
        count = 0
        if file:
            for i in range(0, file.parts_count):
                if file.peer_has_part(Peer.get_local_peer(), i):
                    count +=1
            return count

        else:
            raise Exception("File %s not found" %file_id)


    @classmethod
    def get_peers_for_file_part(cls, file_id, part_num):
        file = cls.find_file_by_id(file_id)
        return file.get_peers_for_file_part(part_num)

    #status can be = ["downloading", "completed", "empty"]
    @classmethod
    def set_status_part_for_file(cls, file_id, part_num, status):
        file = cls.find_file_by_id(file_id)
        if file:
            file.set_peer_status_for_part(Peer.get_local_peer(), part_num, status)
        else:
            raise Exception("File %s not found" %file_id)


    @classmethod
    def create_file_from_parts(cls, file_id):
        klog("TODO: salvare nel HDD il file intero tramite le parti scaricate (se tutte le parti sono scaricate)")

    @classmethod
    def get_filepart_path_from_file(cls, file_id, part_num):
        file = cls.find_file_by_id(file_id)
        if file:
            return "%s/%s.part_%s" %(DOWNLOAD_FOLDER, file.filename, str(part_num))
        else:
            raise Exception("File %s not found" %file_id)
