import os
import sys
import gzip
import socket  # noqa: F401
import threading

class Request:
    def __init__(self, req_bytes):
        self.user_agent = b""
        self.encodings = b""

        line_header, self.body  = req_bytes.split(b"\r\n\r\n")
        
        # parse line_header
        lh_parts = line_header.split(b"\r\n")

        line = lh_parts[0]
        self.headers = [ l.strip() for l in lh_parts[1:]]

        self.verb, self.url, protocol = line.split(b" ")
        self.parse_headers()

    def parse_headers(self):
        for header in self.headers:
            if header.startswith(b"User-Agent:"):
                self.user_agent = header.split(b" ")[1]
            if header.startswith(b"Accept-Encoding:"):
                self.encodings = b" ".join(header.split(b" ")[1:])
                print("header", header)
                print("encodings", self.encodings)

class Headers:
    def __init__(self):
        self.size = None
        self.dtype = None
        self.encoding = None

    def set_size(self, size):
        # int
        self.size = size
    
    def set_dtype(self, dtype):
        # bytes
        self.dtype = dtype

    def set_encoding(self, encoding):
        # bytes
        self.encoding = encoding 

    def get_bytes(self):
        buff = b""
        if self.dtype:
            buff += b"Content-Type: " + self.dtype + b"\r\n"
        if self.size:
            buff += b"Content-Length: " + f"{self.size}\r\n".encode()
        if self.encoding:
            buff += b"Content-Encoding: " + self.encoding + b"\r\n"

        return buff


class Response:
    def __init__(self):
        self.line = None
        self.headers = Headers()
        self.body = None

    def set_status(self, code):
        if code == 200:
            self.line = b"HTTP/1.1 200 OK"
        elif code == 201:
            self.line = b"HTTP/1.1 201 Created"
        elif code == 404:
            self.line = b"HTTP/1.1 404 Not Found"

    def set_body(self, body):
        self.body = body

    def get_message(self):
        body = self.body 
        if b"gzip" == self.headers.encoding:
            body = gzip.compress(body)
            self.headers.set_size(len(body)) 

        message = self.line 
        message += b"\r\n"
        if self.headers:
            message += self.headers.get_bytes()
        message += b"\r\n"
        if self.body:
            message += body

        return message

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    while True:
        conn, address = server_socket.accept() # wait for client
        
        t = threading.Thread(target=handle_client, args=(conn, address))
        t.start()
        

def handle_client(conn, address):
    data = conn.recv(1000)
    print("received \n", data) 
    req = Request(data)

    url = req.url
    res = Response()

    if b"gzip" in req.encodings:
        res.headers.set_encoding(b"gzip")

    if url == b"/":
        res.set_status(200)
    elif url.startswith(b"/echo"):
        
        echo_pl = url[6:]
        
        res.set_status(200)
        res.headers.set_dtype(b"text/plain")
        res.headers.set_size(len(echo_pl))
        
        res.set_body(echo_pl)
    elif url == b"/user-agent":
        res.set_status(200)
        ua = req.user_agent
        res.headers.set_dtype(b"text/plain")
        res.headers.set_size(len(ua))
        res.set_body(ua)        
    elif url.startswith(b"/files") and req.verb == b"GET":
        dir_name = sys.argv[2]
        fname = url[7:]
        fpath = os.path.join(dir_name, fname.decode()) 
        if not os.path.exists(fpath):
            res.set_status(404)
        else:
            with open(fpath, 'rb') as f:
                content = f.read()

            res.set_status(200)
            res.headers.set_size(len(content))
            res.headers.set_dtype(b"application/octet-stream")
            res.set_body(content)
    elif url.startswith(b"/files") and req.verb == b"POST":
        dir_name = sys.argv[2]
        fname = url[7:]
        fpath = os.path.join(dir_name, fname.decode()) 
        with open(fpath, 'wb') as f:
            f.write(req.body)
        res.set_status(201)
    else: 
        res.set_status(404)
    
    message = res.get_message()
    print(message) 
    conn.send(message)


if __name__ == "__main__":
    main()
