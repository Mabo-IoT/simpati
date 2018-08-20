import logging
import time

from socket import socket, AF_INET, SOCK_STREAM


_logger = logging.getLogger(__name__)


class Transition:
    def __init__(self, host, port, block=True):
        self.socket = socket.socket(AF_INET, SOCK_STREAM)
        self.socket.setblocking(block)
        self.addr = (host, port)
        self.connect()

    def connect(self):
        """
        connect to server
        """
        try:
            self.socket.connect(self.addr)
        except ConnectionRefusedError as e:
            raise(e) 

    def send(self, request):
        """
        send requst by socket
        """
        self.socket.send(request)

    def recv(self):
        """
        recv data by socket
        """
        data = self.socket.recv(1024)
        return data
    


    


        