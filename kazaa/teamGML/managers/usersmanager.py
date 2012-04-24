__author__ = 'LucaFerrari MarcoBersani GiovanniLodi'

import mongodbmanager
from custom_utils import hashing
from models.user import User

MY_SESSIONID = ""
IS_SUPER_NODE = ""

class UsersManager(object):

    @classmethod
    def find_user_by_session_id(cls, session_id):
        mongodbmanager.connect()
        return User.objects(session_id=session_id).first()

    @classmethod
    def find_user_by_ip(cls, ip):
        mongodbmanager.connect()
        return User.objects(ip = ip).first()

    @classmethod
    def find_user_by_ip_and_port(cls, ip, port):
        mongodbmanager.connect()
        return User.objects(ip = ip, port = port).first()

    @classmethod
    def create_user(cls, ip, port):
        mongodbmanager.connect()

        new_user = User(ip=str(ip), port=port, session_id=hashing.generate_session_id())
        new_user.save()
        return new_user

    @classmethod
    def delete_user(cls, user):
        mongodbmanager.connect()
        user.delete()


    @classmethod
    def delete_all(cls):
        mongodbmanager.connect()
        User.drop_collection()

    @classmethod
    def get_my_session_id(cls):
        return MY_SESSIONID

    @classmethod
    def set_my_session_id(cls, session_id):
        MY_SESSIONID = session_id

    @classmethod
    def is_super_node(cls):
        return IS_SUPER_NODE

    @classmethod
    def set_is_super_node(cls, is_super_node):
        IS_SUPER_NODE = is_super_node