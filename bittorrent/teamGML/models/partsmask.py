class PartsMask(object):

    def __init__(self, num_parts):
        self.parts = []

        #Fill the mask with all False value
        for i in range(0, num_parts):
            self.parts[i] = False

    def is_available(self, part_num):
        return type(self.parts[part_num]) is bool and self.parts[part_num] == True

    def is_not_started(self, part_num):
        part_status = self.parts[part_num]
        return part_status == False

    def set_available(self, part_num, available):
        self.parts[part_num] = available

    def set_part_status(self, part_num, status):
        if status == "completed":
            self.set_available(part_num, True)
        elif status == "empty":
            self.set_available(part_num, False)
        else:
            self.parts[part_num] = status
