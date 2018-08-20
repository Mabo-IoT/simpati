import logging
import time

from socket import socket, AF_INET, SOCK_STREAM
from simpati.request import Request
from simpati.transition import Transition
from simpati.response import Response

_logger = logging.getLogger(__name__)


class Client:
    def __init__(self, host, port, block=True):
        self.transition = Transition(host, port, block)
    
    def read(self, cmd, chamber_index, *args):
        """
        send cmd
        """
        ## send request and recv res bytes
        request = Request(cmd, chamber_index, *args)
        self.transition.send(request.bytes)
        data_bytes = self.transition.recv()
        ## make response by bytes
        res = Response.make_response(data_bytes)

        return res
        
    
