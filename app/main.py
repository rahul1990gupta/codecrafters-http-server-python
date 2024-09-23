import socket  # noqa: F401

class Request:
    def __init__(self, req_bytes):
        line_header, body  = req_bytes.split(b"\r\n\r\n")
        
        # parse line_header
        lh_parts = line_header.split(b"\r\n")

        line = lh_parts[0]
        self.headers = [ l.strip() for l in lh_parts[1:]]

        self.verb, self.url, protocol = line.split(b" ")
        

class Response:
    def __init__(self):
        pass

    def set_line(self, line):
        self.line = line

    def set_headers(self, headers):
        self.headers = headers

    def set_body(self, body):
        self.body = body

    def get_message(self):
        return self.line + b"\r\n" + self.headers + b"\r\n" + self.body


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    # data = server_socket.recv(48)
    while True:
        conn, address = server_socket.accept() # wait for client
        
        data = conn.recv(100)
        req = Request(data)

        url = req.url
        if url == b"/":
            message = b"HTTP/1.1 200 OK\r\n\r\n"
        elif url.startswith(b"/echo"):
            
            echo_pl = url[6:]
            
            res = Response()
            res.set_line(b"HTTP/1.1 200 OK")
            
            headers = b"Content-Type: text/plain\r\nContent-Length: " + f"{len(echo_pl)}".encode() + b"\r\n" 
            res.set_headers(headers)
            
            res.set_body(echo_pl)
            
            message = res.get_message()
        else: 
            message = b"HTTP/1.1 404 Not Found\r\n\r\n"
        conn.send(message)



if __name__ == "__main__":
    main()
