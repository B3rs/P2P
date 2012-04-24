__author__ = 'LucaFerrari MarcoBersani GiovanniLodi'

import socket
from threading import Thread
from models.peer import Peer
from managers.peersmanager import PeersManager
from managers.packetsmanager import PacketsManager
from managers.filesmanager import FilesManager
from managers.usersmanager import UsersManager
from custom_utils.formatting import *
from custom_utils.hashing import *
from custom_utils.logging import *
from custom_utils.sockets import *
from threads.download_thread import DownloadThread
from threads.service_thread import ServiceThread
import threading

TTL_FOR_SUPERPEERS_SEARCH = 4
TTL_FOR_FILES_SEARCH = 3

class RequestEmitter(object):

    def __init__(self, local_port):
        self.local_port = local_port
        self.ui_handler = None

    def search_for_superpeers(self, ttl = TTL_FOR_SUPERPEERS_SEARCH ):
        klog("Started query flooding for superpeers, ttl %s" %ttl)

        p_id = generate_packet_id(16)
        formatted_port = format_port_number(self.local_port)
        formatted_ttl = format_ttl(ttl)

        for peer in PeersManager.find_known_peers():
            sock = connect_socket(peer.ip, peer.port)
            local_ip = get_local_ip(sock.getsockname()[0])
            PacketsManager.add_new_generated_packet(p_id)
            sock.send("SUPE" + p_id + format_ip_address(local_ip) + formatted_port + formatted_ttl)
            sock.close()

    def search_for_files(self, query, as_supernode = False, ttl = TTL_FOR_FILES_SEARCH ):
        klog("Started query flooding for files: %s ttl: %s" %(query,ttl) )
        p_id = generate_packet_id(16)
        PacketsManager.add_new_generated_packet(p_id)

        if as_supernode:
            # TODO this lines have been moved are here for reference and because there's no handling, plese remove them ASAP
            #---
            for superpeer in PeersManager.find_known_peers(True):
                sock = connect_socket(superpeer.ip, superpeer.port)
                local_ip = get_local_ip(sock.getsockname()[0])
                sock.send("QUER" + p_id + format_ip_address(local_ip) + format_port_number(self.local_port) + format_ttl(ttl) + format_query(query))
                sock.close()
            #---

            ServiceThread.initialize_for_pckt(p_id)    #enable the receive of packets for this query

            def fun(search_id):
                #search_id is the packet id of QUER request, it identifies univocally the query
                superpeers_result = ServiceThread.get_query_results(search_id)
                my_directory_result = FilesManager.find_files_by_query()
                result = {}
                #costruisco l'array di risultati
                for r in superpeers_result:
                    if result.has_key(r.hash):
                        result[r.hash].peers.push[{'ip':r.ip, 'port':r.port}]
                    else:
                        result[r.hash] = {'filemd5':r.hash, 'filename':r.filename, 'peers':[{'ip':r.ip, 'port':r.port}]}

                for f in my_directory_result:
                    u = UsersManager.find_user_by_session_id(f.session_id)
                    if result.has_key(r.hash):
                        result[f.hash].peers.push[{'ip':u.ip, 'port':u.port}]
                    else:
                        result[f.hash] = {'filemd5':f.hash, 'filename':f.filename, 'peers':[{'ip':u.ip, 'port':u.port}]}

                #must send AFIN
                sock = connect_socket(superpeer.ip, superpeer.port)
                local_ip = get_local_ip(sock.getsockname()[0])
                sock.send("AFIN"+format_deletenum(len(result)))
                for r in result:
                    sock.send(decode_md5(r.filemd5))
                    sock.send(format_filename(r.filename))
                    sock.send(format_deletenum(len(r.peers)))
                    for peer in r.peers:
                        sock.send(format_ip_address(peer.ip))
                        sock.send(format_port_number(peer.port))
                sock.close()

            threading.Timer(20, fun, args=(p_id,)).start()  #calls the fun function with p_id as argument
        else:
            my_superpeer = PeersManager.find_my_superpeer()
            sock = connect_socket(my_superpeer.ip, my_superpeer.port)
            local_ip = get_local_ip(sock.getsockname()[0])
            sock.send("FIND" + p_id + format_ip_address(local_ip) + format_port_number(self.local_port) + format_ttl(ttl) + format_query(query))
            sock.close()

    def download_file(self, peer_ip, peer_port, md5, filename):
        downloadSocket = connect_socket(peer_ip, peer_port)
        downloadSocket.send("RETR")
        downloadSocket.send(decode_md5(md5))
        # Star a thread that will take care of the download and of the socket management
        dlThread = DownloadThread(downloadSocket, filename, md5, peer_ip, self.ui_handler)
        dlThread.start()
