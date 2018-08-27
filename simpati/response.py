import logging
import time
import struct


_logger = logging.getLogger(__name__)

SR = int(182)
CR = int(13)


class Response:
    def __init__(self, contents, cmd, charmber_index, *args):
        """
        all params in bytes
        """
        self.contents = contents
        self.cmd = cmd
        self.chamber_index = charmber_index
        self.num = args[0]

    @classmethod   
    def make_response(cls, bytes_data, cmd, charmber_index, *args):
        """
        make response by classmethod
        """
        bytes_list = bytes_data.split(b'\r')
        contents = bytes_list[0]
        if contents:
            return cls(contents, cmd, charmber_index, *args)
        else:
            raise NoneDataException("None data is recevied, please check Server connection.")
    
    @property
    def types(self):
        """
        type is error or data
        """
        error_flag = b'-'
        if self.contents.startswith(error_flag):
            return "error"
        
        else:
            return "data"
    
    @property
    def error(self):
        """
        if types is error, need know error text
        """
        error_dict = {
            "-1": "Empty command string",
            "-2": "Missing Chamber-ID",
            "-3": "Invalid Chamber-ID",
            "-4": "Chamber not accessible",
            "-5": "Unknown Command-ID",
            "-6": "Insufficient number or wrong command parameters",
            "-7": "No server (in server service command mode)",
        }

        if self.types == "error":
            error_code = self.contents[:2].decode()
            
            return error_dict.get(error_code, "unknow error code {}".format(error_code))

        else:
            return None

    @property
    def data(self):
        """
        if type is data, need know data text
        '1\xb630.000000
        """
        if self.types == "data":
            print(self.contents)
            data  = self.contents.split(b'\xb6')[1].decode() # data is split by sperator
            
            return data

        else:
            return None


class NoneDataException(Exception):
    pass