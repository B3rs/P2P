__author__ = 'LucaFerrari MarcoBersani GiovanniLodi'

class File(object):
    def __init__(self, path, name, md5):
        self.filepath = path
        self.filename = name
        self.md5 = md5