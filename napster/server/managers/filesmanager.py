import mongodbmanager
from models.file import File
from models.user import User

class FilesManager(object):

    @classmethod
    def find_file_by_query(cls, query):
        #words = query.split(" ")
        #TODO devo implementare il group by md5
        return File.objects(name__icontains = query)

    @classmethod
    def find_file_by_hash_and_sessionid(cls, hash, session_id):
        mongodbmanager.connect()
        return File.objects(hash = hash, session_id = session_id).first()

    @classmethod
    def find_files_by_hash(cls, hash):
        mongodbmanager.connect()
        return File.objects(hash = hash).all()

    @classmethod
    def count_files_by_hash(cls, hash):
        mongodbmanager.connect()
        return File.objects(hash = hash).count()

    @classmethod
    def find_files_for_user(cls, user):
        mongodbmanager.connect()
        return File.objects(session_id = user.session_id)
    
    @classmethod
    def find_file(cls, name, hash, user):
        mongodbmanager.connect()
        return  File.objects(name = name, hash = hash, session_id = user.session_id).first()

    @classmethod
    def create_file(cls, name, hash, user):
        file = cls.find_files_by_hash(hash).first()
        if file is None:
            # Create new file
            newFile = File(name = name, hash = hash, session_id = user.session_id)
            newFile.save()
        else:
            # Update file name
            cls.update_file(file, name)

    @classmethod
    def update_file(cls, file, new_name):
        mongodbmanager.connect()
        file.name = new_name
        file.save()

    @classmethod
    def delete_file(cls, file):
        mongodbmanager.connect()
        file.delete()

    @classmethod
    def delete_files_for_user(cls, user):
        mongodbmanager.connect()
        files = cls.find_files_for_user(user)
        if files is not None:
            count = files.count()
            files.delete()
            return count