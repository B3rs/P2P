__author__ = 'LucaFerrari MarcoBersani GiovanniLodi'

from managers.filesmanager import FilesManager
import socket, os, sys
from threading import Thread
from custom_utils.logging import klog
from custom_utils.hashing import decode_md5, encode_md5


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

    def find_files(self, session_id, query_string):
        files = []
        user = UsersManager.find_user_by_session_id(session_id)
        if user:
            if query_string != "":
                #Exlude all the file that are owened by the current user
                for f in FilesManager.find_files_by_query(query_string):
                    if f.session_id != session_id:
                        files.append(f)
        return files

    def register_download(self, peer_client_session_id, hash, peer_server_ip, peer_server_port):
        user_client = UsersManager.find_user_by_session_id(peer_client_session_id)
        if user_client:
            #Ok valid client, now get the user that served the file to the client
            user_server = UsersManager.find_user_by_ip_and_port(peer_server_ip, peer_server_port)
            file = FilesManager.find_file_by_hash_and_sessionid(hash, user_server.session_id)
            FilesManager.increase_download_count_for_file(file)
            return file.download_count

    def run(self):
        print "thread started"
        self._socket.setblocking(1)

        try:

            self._socket.setblocking(1) # <--------

            command = str(self._socket.recv(4))

            if command == "LOGI":
                peer_ip = str(self._socket.recv(15))
                peer_port = str(self._socket.recv(5))

                if UsersManager.find_user_by_ip(peer_ip) is not None:
                    self._socket.send("ALGI"+"0"*16)
                    klog("Sent ALGI"+"0"*16+"to: %s" %(peer_ip))
                else:
                    session_id = str(self.login_user(peer_ip, peer_port))
                    klog("Received a LOGI, from: %s, port: %s. Session id created: %s" %(peer_ip, peer_port, session_id))
                    self._socket.send("ALGI"+session_id)
                    klog("Sent ALGI to: %s, port: %s" %(peer_ip, peer_port))

            elif command == "ADDF":
                peer_session_id = str(self._socket.recv(16))
                file_hash = encode_md5(self._socket.recv(16))
                file_name = str(self._socket.recv(100)).strip(' ')
                klog("Received a ADDF, from: %s. Hash: %s. Filename: %s." %(peer_session_id, file_hash, file_name))
                copy_num = self.add_file(peer_session_id, file_hash, file_name)
                klog("Files with same hash: %d" %( copy_num))
                self._socket.send("AADD"+"{0:03d}".format(copy_num))
                klog("Sent AADD to: %s. Files copy num: %d" %(peer_session_id, copy_num))

            elif command == "DELF":
                peer_session_id = str(self._socket.recv(16))
                file_hash = encode_md5(self._socket.recv(16))
                copy_num = self.remove_file(peer_session_id, file_hash)
                klog("Received a DELF, from: %s. Hash: %s. Remaining files with same hash: %d" %(peer_session_id, file_hash, copy_num))
                self._socket.send("ADEL"+"{0:03d}".format(copy_num))
                klog("Sent ADEL to: %s" %(peer_session_id))

            elif command == "FIND":
                peer_session_id = str(self._socket.recv(16))
                # We recieve a lot of spaces in the query string, due to the codification rules
                # with .strip we remove the spaces strip
                query_string = str(self._socket.recv(20)).strip(' ')

                klog("Received a FIND, from session_id: %s. Query string: %s" %(peer_session_id, query_string))

                files = self.find_files(peer_session_id, query_string)
                string = "AFIN"+"{0:03d}".format(len(files))

                counter = 4 + 3 # AFIN is 4 + 3 that is the number of bytes for the number of copies

                for file in files:
                    copyes = FilesManager.find_files_by_hash(file.hash)
                    string += decode_md5(file.hash) + str("{0:100s}".format(file.name)) + str("{0:03d}".format(len(copyes)))
                    counter += 16 + 100+ 3

                    for copy in copyes:
                        user = UsersManager.find_user_by_session_id(copy.session_id)
                        string += str(user.ip) + str("{0:05d}".format(user.port))
                        counter += 15 + 5

                if len(string) == counter:
                    self._socket.send(string)
                    klog("Sent %s" %(string))
                else:
                    klog("errore nella ricerca... attendevo %s caratteri e ne genero %s" %(str(counter), str(len(string))))

            elif command == "RREG":
                peer_session_id = str(self._socket.recv(16))
                file_hash = encode_md5(self._socket.recv(16))
                peer_ip = str(self._socket.recv(15))
                peer_port = str(self._socket.recv(5))
                download_num = self.register_download(peer_session_id, file_hash, peer_ip, peer_port)
                self._socket.send("ARRE"+"{0:03d}".format(download_num))

            elif command == "LOGO":
                peer_session_id = str(self._socket.recv(16))
                delete_num = self.logout_user(peer_session_id)
                klog("Received a LOGO, from session_id: %s" %(peer_session_id))
                self._socket.send("ALGO"+"{0:03d}".format(delete_num))
                klog("Sent ALGO to session_id: %s" %(peer_session_id))

            elif command == "":
                condition = False

            self._socket.close()
        except Exception, ex:
            condition = False
            print ex

        print "request processed correctly"

class ClientThread(Thread):
    #questo thread deve essere lanciato all'inizio e non deve mai uscire

    def __init__(self):
        super(ServiceThread, self).__init__()

    #definisco i vari metodi

    def run(self):

        print "started the client thread"

        while 1:
            print "che cosa desideri fare?"
            print "1)cercare un file"
            print "2)aggiornare la lista dei peer"
            cmdn = sys.stdin.read()

            if cmdn == 1:
                pass
            elif cmdn == 2:
                pass
            else:
                print "comando non valido"



class GnutellaPeer(object):

    def __init__(self):
        #Clear all the db
        FilesManager.delete_all()

        self.server_socket = None
        print "Init Gnutella peer"
        self.server_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        if len(sys.argv) > 1 and sys.argv[1] != None:
            port = sys.argv[1]
        else:
            port = 9999
        
        self.server_socket.bind(
            ("0.0.0.0", int(port))
        )

        print "Port: %s" %(port)

    def start(self):
        print "Starting server...."

        #Devo far partire il thread che gestisce la funzioni da client (io sono il client)

        self.server_socket.listen(10)
        while 1:
            print "Waiting for connection "
            (socket_client, address) = self.server_socket.accept()
            s = ServiceThread(socket_client)
            s.start()


if __name__ == "__main__":
    ns = GnutellaPeer()
    ns.start()