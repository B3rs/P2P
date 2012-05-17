class PartsMask(object):

    def __init__(self, num_parts):
        self.parts = []

        #Fill the mask with all False value
        for i in range(0, num_parts):
            self.parts[i] = False

    def is_available(self, part_num):
        return self.parts[part_num]

    def set_available(self, part_num):
        self.parts[part_num] = True