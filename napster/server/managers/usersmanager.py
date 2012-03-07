import mongodbmanager
from custom_utils import hashing
from models.user import User

class UsersManager:

    @classmethod
    def find_user_by_session_id(cls, session_id):
        mongodbmanager.connect()
        return User.objects(session_id=session_id).first()


    @classmethod
    def create_user(cls, ip, port):
        mongodbmanager.connect()

        new_user = User(ip=str(ip), port=port, session_id=hashing.generate_session_id())
        new_user.save()

    @classmethod
    def delete_user(cls, user):
        mongodbmanager.connect()
        user.delete()

