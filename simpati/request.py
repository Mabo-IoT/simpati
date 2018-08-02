import logging
import time
import struct


_logger = logging.getLogger(__name__)

SR = int(182)
CR = int(13)

class Request:
    def __init__(self, cmd, charmber_index, *args):
        """
        args is param_1, 2, 3...up to 4
        """
        self.cmd = cmd
        self.charmber_index = charmber_index
        self.params = args

    @property
    def bytes(self):
        """
        convert request to bytes
        """
        fmt = self.convert_fmt(self.cmd, self.charmber_index, self.params)
        # encode self.params to bytes
        params = [param.encode() for param in self.params]
        
        # insert SR to params 
        # egg.[param1, SR, param2, SR ...]
        for i in range(len(params)):
            params.insert(2*i+1, SR)

        bytes_data = struct.pack(fmt, self.cmd.encode(), SR, self.charmber_index.encode(), SR, *params, CR) 

        return bytes_data

    @staticmethod
    def convert_fmt(command, charmber_index, params):
        """
        convert  struct need format
        """
        # separator
        SR = 182
        # terminator
        CR = 13

        fmt_header = "{0}s1B{1}s1B".format(len(command), len(charmber_index))

        fmt_body = ""
        for param in params:
            
            fmt_body = fmt_body + "{0}s1B".format(len(param))

        fmt_tail = "1B"

        fmt = fmt_header + fmt_body + fmt_tail
        
        return fmt

        
        
        

        