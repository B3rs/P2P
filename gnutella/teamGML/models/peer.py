__author__ = 'LucaFerrari MarcoBersani GiovanniLodi'

from custom_utils.formatting import format_ip_address


class Peer(object):

    def __init__(self, ip, port):
        self.ip = format_ip_address(ip)       # Forced typecast, is this a good idea or bad coding?
        self.port = int(port)   # TODO check for type?