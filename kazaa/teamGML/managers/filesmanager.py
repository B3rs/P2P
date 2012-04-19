__author__ = 'LucaFerrari MarcoBersani GiovanniLodi'
import os
from custom_utils import hashing
from models.file import File
from manager.usersmanager import UserManager

# TODO: WARNING!
# SHARED_PATH = "../shared"
# That way path is defined from this file location, but it doesn't work,
# because the method it's called form another file in a different location...
# TODO find a way to evaluate the path in a way that is transparent to the caller of the method
SHARED_PATH = "../shared"
FILES = []

class FilesManager(object):

    @classmethod
    def load_my_files(cls):
        for dirname, dirnames, filenames in os.walk(SHARED_PATH):
            for filename in filenames:
                path = dirname + "/" + filename
                md5 = hashing.encode_md5(hashing.calculate_md5_for_file_path(path))
                file = File(path, filename, md5, UserManager.get_my_session_id)
                cls.shared_files().append(file)

    @classmethod
    def create_file(cls, name, hash, user):
        file = cls.find_file_by_hash_and_sessionid(hash, user.session_id)
        if file is None:
            # Create new file
            newFile = File("", name, hash, session_id = user.session_id)
            cls.shared_files().append(newFile)
        else:
            # Update file name
            cls.update_file(file, name)

    @classmethod
    def update_file(cls, file, new_name):
        file.filename = new_name

    @classmethod
    def delete_file(cls, file):
        cls.shared_files().remove(file)

    # @returns array with matches path
    @classmethod
    def find_files_by_query(cls, query, shared_path = SHARED_PATH):
        query = query.lower().strip(' ')

        # Loop in the shared files directory and look for occurrence
        matches = []

        for file in cls.shared_files():
            if file.filename.lower().find(query) != -1:
                matches.append(file)
        return matches

    @classmethod
    def find_file_by_hash_and_sessionid(cls, hash, session_id):
        for file in cls.shared_files():
            if file.hash == hash and file.session_id == session_id:
                return file

    @classmethod
    def find_file_by_hash(cls, hash):
        for file in cls.shared_files():
            if file.hash == hash:
                return file
        return False

    @classmethod
    def shared_files(cls):
        return FILES


