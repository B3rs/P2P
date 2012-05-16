__author__ = 'LucaFerrari MarcoBersani GiovanniLodi'

class UsersManager(object):

    MY_SESSIONID = ""
    USERS = []
    MY_TRACKER = None

    @classmethod
    def get_my_session_id(cls):
        return UsersManager.MY_SESSIONID

    @classmethod
    def set_my_session_id(cls, session_id):
        UsersManager.MY_SESSIONID = session_id

    @classmethod
    def set_tracker(cls, peer):
        UsersManager.MY_TRACKER = peer

    @classmethod
    def get_tracker(cls):
        return UsersManager.MY_TRACKER

