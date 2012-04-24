__author__ = 'LucaFerrari MarcoBersani GiovanniLodi'

import socket


def connect_socket(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # useful to avoid boring address already in use
    sock.connect((ip, int(port)))
    return sock

# See http://stackoverflow.com/questions/7334349/python-get-local-ip-address-used-to-send-ip-data-to-a-specific-remote-ip-addres
# TODO use a better self explaining name
def get_local_ip(host):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect((host, 9))
        client = s.getsockname()[0]
    except socket.error:
        client = "Unknown IP"
    finally:
        del s
    return client


def read_from_socket(socket, numToRead): #in ingresso ricevo la socket e il numero di byte da leggere

    lettiTot = socket.recv(numToRead)
    num = len(lettiTot)

    while (num < numToRead):
        letti = socket.recv(numToRead - num)
        num = num + len(letti)
        lettiTot = lettiTot + letti

    return lettiTot #restituisco la stringa letta