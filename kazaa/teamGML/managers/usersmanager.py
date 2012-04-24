__author__ = 'LucaFerrari MarcoBersani GiovanniLodi'


from custom_utils import hashing
from models.user import User

MY_SESSIONID = ""
IS_SUPER_NODE = False
USERS = []
MY_SUPERPEER = None


class UsersManager(object):

    @classmethod
    def find_user_by_session_id(cls, session_id):
        for user in USERS:
            if user.session_id == session_id:
                return user
        return None

    @classmethod
    def find_user_by_ip(cls, ip):
        for user in USERS:
            if user.ip == ip:
                return user
        return None

    @classmethod
    def find_user_by_ip_and_port(cls, ip, port):
        for user in USERS:
            if user.ip == ip and user.port == port:
                return user
        return None

    @classmethod
    def create_user(cls, ip, port):
        user = User(ip, port, hashing.generate_session_id())
        USERS.append(user)
        return user

    @classmethod
    def delete_user(cls, user):
        USERS.remove(user)

    @classmethod
    def delete_all(cls):
        USERS = []

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

    @classmethod
    def set_superpeer(cls, peer):
        MY_SUPERPEER = peer