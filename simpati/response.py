import logging
import time
import struct


_logger = logging.getLogger(__name__)

SR = int(182)
CR = int(13)


class Response:
    def __init__(self, contents):
        """
        all params in bytes
        """
        self.contents = contents

    @classmethod   
    def make_response(cls, bytes_data):
        """
        make response by classmethod
        """
        bytes_list = bytes_data.split(b'\r')
        contents = bytes_list[0]

        return cls(contents)
    
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
