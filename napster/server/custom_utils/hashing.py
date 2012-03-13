__author_ = "gio"

import string
import random

def generate_session_id(size=16):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for x in range(size))