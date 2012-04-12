__author__ = 'LucaFerrari MarcoBersani GiovanniLodi'


def format_ip_address(ip):
    ip_components = str(ip).split(".")
    IP_1 = '%(#)03d' % {"#" : int(ip_components[0])}
    IP_2 = '%(#)03d' % {"#" : int(ip_components[1])}
    IP_3 = '%(#)03d' % {"#" : int(ip_components[2])}
    IP_4 = '%(#)03d' % {"#" : int(ip_components[3])}
    return IP_1 + "." + IP_2 + "." + IP_3 + "." + IP_4 #IP is now formatted

def format_port_number(port):
    return '%(#)05d' % {"#" : int(port)}
