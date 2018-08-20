import unittest

from context import Request, Response


class Test_request(unittest.TestCase):
    def setUp(self):
        """
        init a request instance
        """
        self.cmd = "11004"
        self.charmber_index = "1"
        self.param_1 = "1"
        self.request = Request(self.cmd, self.charmber_index, self.param_1)

    def test_bytes(self):
        """
        test request bytes propery func
        """ 
        bytes_data = self.request.bytes

        SR = int(182).to_bytes(1, "big")
        CR = int(13).to_bytes(1, "big")
        bytes_data_except = memoryview(bytearray(self.cmd.encode()) + bytearray(SR) + bytearray(self.charmber_index.encode()) + 
            bytearray(SR) + bytearray(self.param_1.encode()) + bytearray(SR) + bytearray(CR)).tobytes()

        self.assertEqual(bytes_data_except, bytes_data)

    def test_convert_fmt(self):
        """
        test request convert_fmt func
        """
        cmd = "11004"
        charmber_index = "1"
        params = ["1", "2"]

        fmt = self.request.convert_fmt(cmd, charmber_index, params)
        self.assertEqual("5s1B1s1B1s1B1s1B1B", fmt)
       
        cmd1 = "11004"
        charmber_index1 = "1"
        params1 = ["1"]

        fmt1 = self.request.convert_fmt(cmd1, charmber_index1, params1)
        self.assertEqual("5s1B1s1B1s1B1B", fmt1)


class Test_response(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_make_response(self):
        """
        test Response make_response classmethod func
        """
        bytes_data = b'1\xb630.000000\r\n'
        res = Response.make_response(bytes_data)
        self.assertIsInstance(res, Response)
        self.assertEqual(res.contents, b'1\xb630.000000')

        bytes_data1 = b'1\xb6(002)Act. value defect  EK1/X22        \r\n'
        res1 = Response.make_response(bytes_data1)
        self.assertIsInstance(res1, Response)
        self.assertEqual(res1.contents, b'1\xb6(002)Act. value defect  EK1/X22        ')
    
    def test_error(self):
        """
        test Response types property func
        """
        bytes_data = b'1\xb630.000000\r\n'
        res = Response.make_response(bytes_data)
        self.assertEqual(res.error, None)

        bytes_data = b'-1\r\n'
        res = Response.make_response(bytes_data)
        self.assertEqual(res.error, "Empty command string")

        bytes_data = b'-9\r\n'
        res = Response.make_response(bytes_data)
        self.assertEqual(res.error, "unknow error code -9")

    def test_types(self):
        """
        test Response error property func
        """
        bytes_data = b'1\xb630.000000\r\n'
        res = Response.make_response(bytes_data)
        self.assertEqual(res.types, "data")

        bytes_data = b'-1\r\n'
        res = Response.make_response(bytes_data)
        self.assertEqual(res.types, "error")
    
    def test_data(self):
        """
        test Response data property func
        """
        bytes_data = b'1\xb630.000000\r\n'
        res = Response.make_response(bytes_data)
        self.assertEqual(res.data, "30.000000")

        bytes_data = b'1\xb6(002)Act. value defect  EK1/X22        \r\n'
        res = Response.make_response(bytes_data)
        self.assertEqual(res.data, "(002)Act. value defect  EK1/X22        ")

        bytes_data = b'-1\r\n'
        res = Response.make_response(bytes_data)
        self.assertEqual(res.data, None)

if __name__ == '__main__':
    suite = unittest.TestSuite()
    tests = [Test_request("test_convert_fmt"),Test_request("test_bytes"), Test_response("test_make_response"),Test_response("test_types"),
    Test_response("test_error"), Test_response("test_data"), ]

    suite.addTests(tests)

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)