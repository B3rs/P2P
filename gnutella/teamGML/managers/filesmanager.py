__author__ = 'LucaFerrari MarcoBersani GiovanniLodi'
import os
from custom_utils import hashing
from models.file import File

# TODO: WARNING!
# SHARED_PATH = "../shared"
# That way path is defined from this file location, but it doesn't work,
# because the method it's called form another file in a different location...
# TODO find a way to evaluate the path in a way that is transparent to the caller of the method
SHARED_PATH = "../shared"
FILES = []

class FilesManager(object):

    @classmethod
    def load_files(cls):
        for dirname, dirnames, filenames in os.walk(SHARED_PATH):
            for filename in filenames:
                path = dirname + "/" + filename
                md5 = hashing.encode_md5(hashing.calculate_md5_for_file_path(path))
                file = File(dirname, filename, md5)
                FILES.append(file)

    # @returns array with matches path
    @classmethod
    def find_files_by_query(cls, query, shared_path = SHARED_PATH):

        query = query.lower().strip(' ')

        # Loop in the shared files directory and look for occurrence
        matches = []

        for file in FILES:
            if file.filename.lower().find(query) != -1:
                matches.append(file)
        return matches

    @classmethod
    def find_file_by_md5(cls, md5):
        for file in FILES:
            if file.md5 == md5:
                return file
        return False

    @classmethod
    def shared_files(cls):
        return FILES
