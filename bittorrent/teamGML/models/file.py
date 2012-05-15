__author__ = 'LucaFerrari MarcoBersani GiovanniLodi'

import os, math

DEFAULT_PART_SIZE = 256

class File(object):
    def __init__(self, path, name, id):
        self.filepath = path
        self.filename = name
        self.id = id

        self.file_size = os.path.getsize(self.full_filepath())

        if self.file_size > DEFAULT_PART_SIZE:
            self.part_size = 256
        else:
            self.part_size = self.file_size

        self.parts_count = math.ceil(self.file_size / self.part_size)

    def full_filepath(self):
        return self.filepath+"/"+self.filename
