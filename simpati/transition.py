import logging
import time
import asyncio

# from socket import socket, AF_INET, SOCK_STREAM


_logger = logging.getLogger(__name__)


class Transition:    
    @classmethod
    async def create(cls, host, port, loop):
        self = Transition()
        try:
            self.reader, self.writer = await asyncio.open_connection(host=host, port=port, loop=loop) 
        except ConnectionError as e:
            raise e
        return self

    def send(self, request):
        """
        send requst by socket
        """
        self.writer.write(request)

    def recv(self):
        """
        recv data by socket
        """
        data = self.reader.read(1024)
        return data
    
    def close(self):
        """
        close connection
        """
        self.writer.close()
    


    


        