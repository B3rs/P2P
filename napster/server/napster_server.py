from managers.filesmanager import FilesManager
from managers.usersmanager import UserManager
import socket, os
from threading import Thread


class ServiceThread(Thread):
    def __init__(self, socket):
        self._socket = socket
        super(ServiceThread, self).__init__()

    def login_user(self, ipp2p, pp2p):
        #UserManager.create_user("123123", "ssss")
        print "tdb"
        session_id = "1234567812345678"
        return session_id

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
        print "trhead started"
        while 1:
            try:
                command = str(self._socket.recv(4))

                if command == "LOGI":
                    peer_ip = str(self._socket.recv(15))
                    peer_port = str(self._socket.recv(5))
                    session_id = str(self.login_user(peer_ip, peer_port))
                    self._socket.send("ALOG"+session_id)

                elif command == "ADDF":
                    peer_session_id = str(self._socket.recv(16))
                    file_md5 = str(self._socket.recv(16))
                    file_name = str(self._socket.recv(100))
                    copy_num = self.add_file(peer_session_id, file_md5, file_name)
                    self._socket.send("AADD"+copy_num)

                elif command == "DELF":
                    peer_session_id = str(self._socket.recv(16))
                    file_md5 = str(self._socket.recv(16))
                    copy_num = self.remove_file(peer_session_id, file_md5)
                    self._socket.send("ADEL"+copy_num)

                elif command == "FIND":
                    peer_session_id = str(self._socket.recv(16))
                    query_string = str(self._socket.recv(20))
                    result = self.find_file(peer_session_id, query_string)
                    print "tbd"
                    #self._socket.send("AFIN"+)

                elif command == "RREG":
                    peer_session_id = str(self._socket.recv(16))
                    file_md5 = str(self._socket.recv(16))
                    peer_ip = str(self._socket.recv(15))
                    peer_port = str(self._socket.recv(5))
                    download_num = self.register_download(peer_session_id, file_md5, peer_ip, peer_port)
                    self._socket.send("ARRE"+download_num)

                elif command == "LOGO":
                    peer_session_id = str(self._socket.recv(16))
                    delete_num = self.find_file(peer_session_id, query_string)
                    self._socket.send("ALGO"+delete_num)

            except Exception, e:
                print e
                break


class NapsterServer(object):

    def __init__(self):
        self.server_socket = None
        print "Init Napster server"
        self.server_socket = socket.socket(
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
            s = ServiceThread(socket_client)
            s.start()


if __name__ == "__main__":
    ns = NapsterServer()
    ns.start()
    print "fine"
