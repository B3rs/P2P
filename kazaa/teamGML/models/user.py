__author__ = 'LucaFerrari MarcoBersani GiovanniLodi'


class User(object):

    def __init__(self, ip, port, session_id):
        self.ip = ip
        self.port = port
        self.session_id = session_id
