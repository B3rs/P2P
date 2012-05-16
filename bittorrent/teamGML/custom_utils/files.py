def file_size(path):
    f = open(path, 'r')
    f.seek(0, 2)
    sz = f.tell()
    f.seek(0, 0)
    f.close()
    return sz
