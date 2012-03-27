__author__ = 'LucaFerrari MarcoBersani GiovanniLodi'

import string
import random
import base64

def generate_session_id(size=16):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for x in range(size))


def encode_md5(md5_string):
    return base64.b64encode(md5_string)

def decode_md5(data):
    return base64.b64decode(data)
