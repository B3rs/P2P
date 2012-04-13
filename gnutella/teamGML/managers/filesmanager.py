__author__ = 'LucaFerrari MarcoBersani GiovanniLodi'
import os
from custom_utils import hashing

# TODO: WARNING!
# SHARED_PATH = "../shared"
# That way path is defined from this file location, but it doesn't work,
# because the method it's called form another file in a different location...
# TODO find a way to evaluate the path in a way that is transparent to the caller of the method
SHARED_PATH = "../shared"


class FilesManager(object):

    # @returns array with matches path
    @classmethod
    def find_files_by_query(cls, query, shared_path = SHARED_PATH):

        query = query.lower().strip(' ')

        # Loop in the shared files directory and look for occurrence
        matches = []

        for dirname, dirnames, filenames in os.walk(shared_path):
            for filename in filenames:
                if filename.lower().find(query) != -1:
                    matches.append(os.path.join(dirname, filename))

        return matches

    # TODO efficiency!!!
    @classmethod
    def find_file_by_md5(cls, md5):
        for dirname, dirnames, filenames in os.walk(SHARED_PATH):
            for filename in filenames:
                path = dirname + "/" + filename
                fileMd5 = hashing.calculate_md5_for_file_path(path)
                if fileMd5 == md5:
                    return path
        return False

    @classmethod
    def shared_files(cls):
        results = []
        for dirname, dirnames, filenames in os.walk(SHARED_PATH):
            for filename in filenames:
                results.append(filename)
        return results
