__author__ = 'LucaFerrari MarcoBersani GiovanniLodi'

import socket
from threading import Thread
from models.peer import Peer
from managers.peersmanager import PeersManager
from managers.packetsmanager import PacketsManager
from custom_utils.formatting import *
from custom_utils.hashing import *
from custom_utils.logging import *
from custom_utils.sockets import connect_socket
from threads.download_thread import DownloadThread

TTL_FOR_PEERS_SEARCH = 3
TTL_FOR_FILES_SEARCH = 3

class RequestEmitter(object):

    def __init__(self, local_port):
        self.local_port = local_port
        self.ui_handler = None

    def search_for_peers(self, ttl = TTL_FOR_PEERS_SEARCH ):
        klog("Started query flooding for peers, ttl %s" %ttl)
        for peer in PeersManager.find_known_peers():
            sock = connect_socket(peer.ip, peer.port)
            local_ip = sock.getsockname()[0]
            p_id = generate_packet_id(16)
            PacketsManager.add_new_generated_packet(p_id)
            sock.send("NEAR" + p_id + format_ip_address(local_ip) + format_port_number(self.local_port) + format_ttl(ttl))
            sock.close()

    def search_for_files(self, query, ttl = TTL_FOR_FILES_SEARCH ):
        klog("Started query flooding for files: %s ttl: %s" %(query,ttl) )
        p_id = generate_packet_id(16)

        for peer in PeersManager.find_known_peers():
            sock = connect_socket(peer.ip, peer.port)
            local_ip = sock.getsockname()[0]
            PacketsManager.add_new_generated_packet(p_id)
            sock.send("QUER" + p_id + format_ip_address(local_ip) + format_port_number(self.local_port) + format_ttl(ttl) + format_query(query))
            sock.close()

    def download_file(self, peer_ip, peer_port, md5, filename):
        downloadSocket = connect_socket(peer_ip, peer_port)
        downloadSocket.send("RETR")
        downloadSocket.send(decode_md5(md5))
        # Star a thread that will take care of the download and of the socket management
        dlThread = DownloadThread(downloadSocket, filename, md5, peer_ip, self.ui_handler)
        dlThread.start()
