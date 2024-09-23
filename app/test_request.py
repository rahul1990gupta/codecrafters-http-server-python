from app.main import Request 
import unittest 

class TestRequest(unittest.TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass

    def test_parse_request(self):
        data = b"GET /echo/abc HTTP/1.1\r\nHost: localhost:4221\r\nUser-Agent: curl/7.64.1\r\nAccept: */*\r\n\r\n"
        req = Request(data)

        self.assertEqual(req.url, b"/echo/abc")
        self.assertEqual(req.verb, b"GET")

    def test_encoding(self):
        data = b"GET /echo/pineapple HTTP/1.1\r\nHost: localhost:4221\r\nAccept-Encoding: gzip\r\n\r\n"
        req = Request(data)

        self.assertEqual(req.encodings, b"gzip")
