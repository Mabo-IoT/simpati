import logging
import time

from socket import socket, AF_INET, SOCK_STREAM
from simpati.request import Request

_logger = logging.getLogger(__name__)


class Client:
    def __init__(self, host, port):
        pass

    
    def send(self, cmd, chamber_index, param_1, *args):
        """
        send cmd
        """
        request = Request()
        
        pass