__author__ = 'luca'

from models.file import File

class FilesManager:

    @classmethod
    def find_by_query(cls, query):
        print "Find files from query: "+query
        return []

    @classmethod
    def create_file(cls, name, hash, session_id):
        f = File(name, hash, session_id)
