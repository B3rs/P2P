__author__ = 'LucaFerrari MarcoBersani GiovanniLodi'

class File(object):
    def __init__(self, path, name, hash, session_id):
        self.filepath = path
        self.filename = name
        self.hash = hash
        self.session_id = session_id