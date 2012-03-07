__author__ = 'luca'

from models.file import File
from models.user import User

class FilesManager:

    @classmethod
    def find_file_by_query(cls, query):
        print "TODO: Find files from DB query: "+query
        return []

    @classmethod
    def find_file_by(cls, name, hash, user):
        print "TODO, get the file from the DB"
        return None

    @classmethod
    def create_file(cls, name, hash, user):
        if find_by(name, hash, user) == None:
            update_file(name, hash, user)
        else:
            f = File(name, hash, user.session_id)
            #save file to db

    @classmethod
    def update_file(cls, file, new_name):
        file.name = new_name
        #save file to db

