class User:

    def __init__(self, ip, port):
        self._ip = ip
        self._port = port

    def destroy(self):
        print "destroy tdb"

    @property
    def ip(self):
        return self._ip

    @property
    def port(self):
        return self._port
