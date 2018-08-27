from socketserver import BaseRequestHandler, TCPServer
from threading import Thread
import time
import random
import struct


SR = int(182).to_bytes(1, "big")
CR = int(13).to_bytes(1, "big")


class simpatiHandler(BaseRequestHandler):
    def handle(self):
        print('Got connection from', self.client_address)
        while True:
            msg = self.request.recv(1024)
            if not msg:
                break
            data = self.parse(msg)
            
            time.sleep(1)
            self.request.send(data)
    
    def parse(self, msg):
        """
        parse msg to requset
        """
        cmd = msg.split(SR)[0].decode()
        if cmd == "17009" or cmd == "14003":
            return self.random_status()
        
        else:
            return self.random_value()
    
    def random_status(self):
        """
        return random response of value
        """
        status = random.randint(0, 1)
        resp = self.make_response_bytes(str(status))
        return resp

    def random_value(self):
        """
        return random response of status
        """
        value = round(random.uniform(20,30), 2)
        resp = self.make_response_bytes(str(value))
        return resp

    def make_response_bytes(self, string_data):
        """
        make a response bytes
        """
        header = str(random.randint(0,1)).encode()
        string_data = string_data.encode()
        END = b'\n'
        fmt = "{0}s{1}s{2}s{3}s1s".format(1,1,len(string_data),1)
        data = struct.pack(fmt, header, SR, string_data, CR, END)
        return data


if __name__ == '__main__':
    serv = TCPServer(('', 20000), simpatiHandler)
    MAXWORKERS = 16
    for n in range(MAXWORKERS):
        t = Thread(target=serv.serve_forever)
        t.daemon = True
        t.start()
    serv.serve_forever()
