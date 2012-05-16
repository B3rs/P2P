__author__ = 'LucaFerrari MarcoBersani GiovanniLodi'
import os
from custom_utils import hashing
from models.file import File
from managers.usersmanager import UsersManager

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
        for dirname, dirnames, filenames in os.walk(SHARED_PATH):
            for filename in filenames:
                path = dirname + "/" + filename
                file = File(path, filename, hashing.generate_file_id())
                cls.shared_files().append(file)

    @classmethod
    def create_file(cls, name, hash, user):
        klog("TBD")
        file = cls.find_file_by_hash_and_sessionid(hash, user.session_id)
        if file is None:
            # Create new file
            newFile = File("", name, hash, session_id = user.session_id)
            cls.shared_files().append(newFile)
        else:
            # Update file name
            cls.update_file(file, name)

    @classmethod
    def delete_file(cls, file):
        cls.shared_files().remove(file)


    @classmethod
    def find_file_by_id(cls, id):
        for file in cls.shared_files():
            if file.id == id:
                return file
        return None

    @classmethod
    def shared_files(cls):
        return FilesManager.FILES
