from managers.filesmanager import FilesManager
from managers.usersmanager import UsersManager
import socket, os
from threading import Thread
from custom_utils.logging import klog
from custom_utils.hashing import read_md5


class ServiceThread(Thread):
    def __init__(self, socket):
        self._socket = socket
        super(ServiceThread, self).__init__()

    def login_user(self, ip, port):
        user = UsersManager.create_user(ip, port)
        return user.session_id

    def logout_user(self, session_id):
        user = UsersManager.find_user_by_session_id(session_id)
        if user:
            numdeleted = FilesManager.delete_files_for_user(user)
            UsersManager.delete_user(user)
            return numdeleted
        else:
            return -1

    def add_file(self, session_id, hash, file_name):
        user = UsersManager.find_user_by_session_id(session_id)
        if user:
            FilesManager.create_file(file_name, hash, user)
        return FilesManager.count_files_by_hash(hash)

    def remove_file(self, session_id, hash):
        file = FilesManager.find_file_by_hash_and_sessionid(hash, session_id)
        if file:
            FilesManager.delete_file(file)
        return FilesManager.count_files_by_hash(hash)

    def find_file(self, session_id, query_string):
        if query_string != "":
            return FilesManager.find_file_by_query(query_string)
        return False

    def register_download(self, session_id, md5, peer_ip, peer_port):
        pass
        #return download_number

    def run(self):
        print "thread started"
        self._socket.setblocking(1)
        condition = True
        while condition:
            try:
                #TODO: cambiare questo perche la recv tenta di leggere byte anche se non ce ne sono e va in loop, che si fa?
                #TODO: Luca la chiamata a recv e' bloccante... se non ci sono dati il while e' bloccato in teoria!


                # TODO Qui si da per scontato che tutti i messaggi ricevuti dal client siano corretti se avanza tempo implementare check sulla sintassi

                self._socket.setblocking(1) # <--------
                
                command = str(self._socket.recv(4))

                if command == "LOGI":
                    peer_ip = str(self._socket.recv(15))
                    peer_port = str(self._socket.recv(5))
                    session_id = str(self.login_user(peer_ip, peer_port))
                    klog("Received a LOGI, from: %s, port: %s. Session id created: %s" %(peer_ip, peer_port, session_id))
                    self._socket.send("ALGI"+session_id)
                    klog("Sent ALGI to: %s, port: %s" %(peer_ip, peer_port))

                elif command == "ADDF":
                    peer_session_id = str(self._socket.recv(16))
                    file_hash = read_md5(self._socket.recv(16))
                    file_name = str(self._socket.recv(100))
                    klog("Received a ADDF, from: %s. Hash: %s. Filename: %s." %(peer_session_id, file_hash, file_name))
                    copy_num = self.add_file(peer_session_id, file_hash, file_name)
                    klog("Files with same hash: %d" %( copy_num))
                    self._socket.send("AADD"+"{0:03d}".format(copy_num))
                    klog("Sent AADD to: %s. Files copy num: %d" %(peer_session_id, copy_num))

                elif command == "DELF":
                    peer_session_id = str(self._socket.recv(16))
                    file_hash = read_md5(self._socket.recv(16))
                    copy_num = str(self.remove_file(peer_session_id, file_hash))
                    klog("Received a DELF, from: %s. Hash: %s. Remaining files with same hash: %d" %(peer_session_id, file_hash, copy_num))
                    self._socket.send("ADEL"+"{0:03d}".format(copy_num))
                    klog("Sent ADEL to: %s" %(peer_session_id))

                elif command == "FIND":
                    peer_session_id = str(self._socket.recv(16))
                    query_string = str(self._socket.recv(20))

                    files = self.find_file(peer_session_id, query_string)

                    string = "AFIN"+"{0:03d}".format(len(files))

                    counter = 4 + 3

                    for file in files:
                        copyes = FilesManager.find_files_by_hash(file.hash)
                        string += str(file.hash) + str("{0:100s}".format(file.name)) + str("{0:03d}".format(len(copyes)))
                        counter += 16 + 100+ 3
                        for copy in copyes:
                            user = UsersManager.find_user_by_session_id(copy.session_id)
                            string += str(user.ip) + str("{0:05d}".format(user.port))
                            counter += 15 + 5

                    if len(string) == counter:
                        self._socket.send(string)
                    else:
                        klog("errore nella ricerca... attendevo %s caratteri e ne genero %s" %(str(counter), str(len(string))))

                elif command == "RREG":
                    peer_session_id = str(self._socket.recv(16))
                    file_hash = read_md5(self._socket.recv(16))
                    peer_ip = str(self._socket.recv(15))
                    peer_port = str(self._socket.recv(5))
                    download_num = self.register_download(peer_session_id, file_hash, peer_ip, peer_port)
                    self._socket.send("ARRE"+"{0:03d}".format(download_num))

                elif command == "LOGO":
                    peer_session_id = str(self._socket.recv(16))
                    delete_num = self.logout_user(peer_session_id)
                    klog("Received a LOGO, from session_id: %s" %(session_id))
                    self._socket.send("ALGO"+"{0:03d}".format(delete_num))
                    klog("Sent ALGO to session_id: %s" %(session_id))
                elif command == "":
                    condition = False

            except Exception, ex:
                condition = False
                print ex
        self._socket.close()
        print "exiting thread"


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
        while 1:
            print "Waiting for connection "
            (socket_client, address) = self.server_socket.accept()
            s = ServiceThread(socket_client)
            s.start()


if __name__ == "__main__":
    ns = NapsterServer()
    ns.start()
    print "fine"
