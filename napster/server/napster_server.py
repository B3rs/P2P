from managers.filesmanager import FilesManager
from managers.usersmanager import UserManager

class NapsterServer:
    def __init__(self):
        print "Init Napster server"

    def start(self):
        print "Starting server...."
        print "Started, waiting for connection"

    def login_user(self, socket):
        UserManager.create_user("123123", "ssss")
        print "tdb"

    def logout_user(self, socket):
        print "tdb"

    def add_file(self, socket):
        FilesManager.create_file("prova", "sssss", "ssss")
        print "tdb"

    def remove_file(self, socket):
        print "tdb"

    def find_file(self, socket):
        print "tdb"

    def download_file(self, socket):
        print "tdb"

if __name__ == "__main__":
    ns = NapsterServer()
    ns.start()
    print "fine"
