__author__ = 'LucaFerrari MarcoBersani GiovanniLodi'

class Peer(object):

    def __init__(self, ip, port):
        self.ip = str(ip)       # Forced typecast, is this a good idea or bad coding?
        self.port = int(port)   # TODO check for type?