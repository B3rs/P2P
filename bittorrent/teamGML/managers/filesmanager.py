from custom_utils.logging import klog

__author__ = 'LucaFerrari MarcoBersani GiovanniLodi'
import os
from custom_utils import hashing
from models.file import File
from models.peer import Peer
from custom_utils.logging import klog
from configurations import PORT



# TODO: WARNING!
# That way path is defined from this file location, but it doesn't work,
# because the method it's called form another file in a different location...
# TODO find a way to evaluate the path in a way that is transparent to the caller of the method
#SHARED_PATH = "../shared" # If u are a normal person
SHARED_PATH = "shared"  # If u are GIO


class FilesManager(object):

    FILES = []

    @classmethod
    def load_my_files(cls):
        peer_me = Peer("127.0.0.0", PORT)
        for dirname, dirnames, filenames in os.walk(SHARED_PATH):
            for filename in filenames:
                path = dirname + "/" + filename
                file = File(hashing.generate_file_id(), filename,path)

                #Set that I have all this file
                for p in range(0, file.parts_count):
                    file.set_peer_has_part(peer_me, p)

                cls.get_files().append(file)

    @classmethod
    def create_file(cls, name, hash, user):
        klog("TBD")
        file = cls.find_file_by_hash_and_sessionid(hash, user.session_id)
        if file is None:
            # Create new file
            newFile = File(hash, name, "")
            cls.shared_files().append(newFile)
        else:
            # Update file name
            cls.update_file(file, name)

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
    def get_ordered_parts_number(cls, file_id):
        file = cls.find_file_by_id(file_id)
        if file:
            klog("TODO: ordinare gli indici delle parti da quella meno conosciuta a quella piu conosciuta")

            return range(0, file.parts_count)

    @classmethod
    def get_files(cls):
        return FilesManager.FILES
