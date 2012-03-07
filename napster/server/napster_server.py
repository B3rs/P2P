from managers.filesmanager import FilesManager
from managers.usersmanager import UserManager
import socket, os

class ServiceThread:
    def __init__(self,socket):
        self._socket = socket

    def login_user(self, ipp2p, pp2p):
        UserManager.create_user("123123", "ssss")
        print "tdb"
        #return session_id

    def logout_user(self, socket):
        print "tdb"

    def add_file(self, session_id, md5, file_name):
        FilesManager.create_file("prova", "sssss", "ssss")
        print "tdb"
        #return copy_number

    def remove_file(self, session_id, md5):
        print "tdb"
        #return copy_number

    def find_file(self, session_id, query_string):
        print "tdb"
        #return varia roba

    def register_download(self, session_id, md5, peer_ip, peer_port):
        pass
        #return download_number

    def run(self):
        while 1:
            try:
                command = str(self._socket.read(4))

                if command == "LOGI":
                    peer_ip = str(self._socket.recv(15))
                    peer_port = str(self._socket.recv(5))
                    session_id = str(self.login_user(peer_ip, peer_port))
                    socket.send("ALGI"+session_id)

                elif command == "ADDF":
                    peer_session_id = str(self._socket.recv(16))
                    file_md5 = str(self._socket.recv(16))
                    file_name = str(self._socket.recv(100))
                    copy_num = self.add_file(peer_session_id, file_md5, file_name)
                    socket.send("AADD"+copy_num)

                elif command == "DELF":
                    peer_session_id = str(self._socket.recv(16))
                    file_md5 = str(self._socket.recv(16))
                    copy_num = self.remove_file(peer_session_id, file_md5)
                    socket.send("ADEL"+copy_num)

                elif command == "FIND":
                    peer_session_id = str(self._socket.recv(16))
                    query_string = str(self._socket.recv(20))
                    result = self.find_file(peer_session_id, query_string)
                    print "tbd"
                    #socket.send("AFIN"+)

                elif command == "RREG":
                    peer_session_id = str(self._socket.recv(16))
                    file_md5 = str(self._socket.recv(16))
                    peer_ip = str(self._socket.recv(15))
                    peer_port = str(self._socket.recv(5))
                    download_num = self.register_download(peer_session_id, file_md5, peer_ip, peer_port)
                    socket.send("ARRE"+download_num)

                elif command == "LOGO":
                    peer_session_id = str(self._socket.recv(16))
                    delete_num = self.find_file(peer_session_id, query_string)
                    socket.send("ALGO"+delete_num)


            except Exception, e:
                print e
                break


class NapsterServer:

    def __init__(self):
        self.server_socket = None
        print "Init Napster server"
        server_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )
        self.server_socket.bind(
            ("0.0.0.0", #socket.gethostname()
             9999)
        )

    def start(self):
        print "Starting server...."
        self.server_socket.listen(10)
        print "Started, waiting for connection"
        while 1:
            (socket_client, address) = self.server_socket.accept()

            socket_client.recv






if __name__ == "__main__":
    ns = NapsterServer()
    ns.start()
    print "fine"
