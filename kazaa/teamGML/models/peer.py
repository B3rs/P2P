__author__ = 'LucaFerrari MarcoBersani GiovanniLodi'

from custom_utils.formatting import format_ip_address, format_port_number


class Peer(object):

    def __init__(self, ip, port, is_superpeer=False):
        self.ip = format_ip_address(ip)
        self.port = format_port_number(port)
        self.is_superpeer = is_superpeer