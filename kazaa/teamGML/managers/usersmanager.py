__author__ = 'LucaFerrari MarcoBersani GiovanniLodi'


from custom_utils import hashing
from models.user import User

class UsersManager(object):

    MY_SESSIONID = ""
    IS_SUPER_NODE = None
    USERS = []
    MY_SUPERPEER = None


    @classmethod
    def find_user_by_session_id(cls, session_id):
        for user in UsersManager.USERS:
            if user.session_id == session_id:
                return user
        return None

    @classmethod
    def find_user_by_ip(cls, ip):
        for user in UsersManager.USERS:
            if user.ip == ip:
                return user
        return None

    @classmethod
    def find_user_by_ip_and_port(cls, ip, port):
        for user in UsersManager.USERS:
            if user.ip == ip and user.port == port:
                return user
        return None

    @classmethod
    def create_user(cls, ip, port):
        user = User(ip, port, hashing.generate_session_id())
        UsersManager.USERS.append(user)
        return user

    @classmethod
    def delete_user(cls, user):
        UsersManager.USERS.remove(user)

    @classmethod
    def delete_all(cls):
        UsersManager.USERS = []

    @classmethod
    def get_my_session_id(cls):
        return UsersManager.MY_SESSIONID

    @classmethod
    def set_my_session_id(cls, session_id):
        UsersManager.MY_SESSIONID = session_id

    @classmethod
    def is_super_node(cls):
        return UsersManager.IS_SUPER_NODE

    @classmethod
    def set_is_super_node(cls, is_super_node):
        UsersManager.IS_SUPER_NODE = is_super_node

    @classmethod
    def set_superpeer(cls, peer):
        UsersManager.MY_SUPERPEER = peer

    @classmethod
    def get_superpeer(cls):
        return UsersManager.MY_SUPERPEER

