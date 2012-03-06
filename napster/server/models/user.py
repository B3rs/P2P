class User:

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def destroy(self):
        print "destroy tdb"
