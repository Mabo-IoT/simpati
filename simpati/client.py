import logging
import time

from socket import socket, AF_INET, SOCK_STREAM
from simpati.request import Request
from simpati.transition import Transition
from simpati.response import Response, NoneDataException

_logger = logging.getLogger(__name__)


class Client:    
    @classmethod
    async def create(cls, host, port, loop):
        self = Client()
        try:
            self.transition = await Transition.create(host, port, loop)
        
        except ConnectionError as e:
            raise e
        
        return self
    
    async def read(self, cmd, chamber_index, *args):
        """
        send cmd
        """
        ## send request and recv res bytes
        request = Request(cmd, chamber_index, *args)
        self.transition.send(request.bytes)
        # recv bytes data
        try:
            data_bytes = await self.transition.recv()
        except Exception as e:
            raise e
        ## make response by bytes
        try:
            res = Response.make_response(data_bytes, cmd, chamber_index, *args)
        except NoneDataException as e:
            raise e
            
        return res
    
    def close(self):
        """
        destroy transition
        """
        self.transition.close()
        del(self.transition)
        
    
