__author_ = "gio"

import string
import random
import binascii
import base64

def generate_session_id(size=16):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for x in range(size))



## {{{ http://code.activestate.com/recipes/496969/ (r1)
#convert string to hex
def toHex(s):
    lst = []
    for ch in s:
        hv = hex(ord(ch)).replace('0x', '')
        if len(hv) == 1:
            hv = '0'+hv
        lst.append(hv)

    return reduce(lambda x,y:x+y, lst)

#convert hex repr to string
def toStr(s):
    return s and chr(atoi(s[:2], base=16)) + toStr(s[2:]) or ''
## end of http://code.activestate.com/recipes/496969/ }}}



def encode_md5(md5_string):
    return base64.b64encode(md5_string)

def decode_md5(data):
    return base64.b64decode(data)
