__author__ = 'LucaFerrari MarcoBersani GiovanniLodi'

import string
import random
import base64
import hashlib

def generate_session_id(size=16):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for x in range(size))

def generate_packet_id(size=16):
    return generate_session_id(size)

def encode_md5(md5_string):
    return base64.b64encode(md5_string)

def decode_md5(data):
    return base64.b64decode(data)

def calculate_md5_for_file_path(path):
    try:
        f = open(path)
        md5 = hashlib.md5()
        while True:
            data = f.read(128)
            if not data:
                break
            md5.update(data)
        return md5.digest()
    except Exception, expt:
        print "Error: %s" % expt

