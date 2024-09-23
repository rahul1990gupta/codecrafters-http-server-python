import socket  # noqa: F401
import threading

class Request:
    def __init__(self, req_bytes):
        line_header, body  = req_bytes.split(b"\r\n\r\n")
        
        # parse line_header
        lh_parts = line_header.split(b"\r\n")

        line = lh_parts[0]
        self.headers = [ l.strip() for l in lh_parts[1:]]

        self.verb, self.url, protocol = line.split(b" ")
    
    def get_user_agent(self):
        for header in self.headers:
            if header.startswith(b"User-Agent:"):
                return header.split(b" ")[1]

       

class Response:
    def __init__(self):
        self.line = None
        self.headers = None
        self.body = None

    def set_status(self, code):
        if code == 200:
            self.line = b"HTTP/1.1 200 OK"
        elif code == 404:
            self.line = b"HTTP/1.1 404 Not Found"

    def set_headers(self, size):
        headers = b"Content-Type: text/plain\r\nContent-Length: " + f"{size}".encode() + b"\r\n" 
        self.headers = headers

    def set_body(self, body):
        self.body = body

    def get_message(self):
        message = self.line 
        message += b"\r\n"
        if self.headers:
            message += self.headers
        message += b"\r\n"
        if self.body:
            message += self.body

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
    data = conn.recv(100)
    req = Request(data)

    url = req.url
    res = Response()
    if url == b"/":
        res.set_status(200)
        message = res.get_message()
    elif url.startswith(b"/echo"):
        
        echo_pl = url[6:]
        
        res = Response()
        res.set_status(200)
        res.set_headers(len(echo_pl))
        
        res.set_body(echo_pl)
        
        message = res.get_message()
    elif url == b"/user-agent":
        res.set_status(200)
        ua = req.get_user_agent()
        res.set_headers(len(ua))
        res.set_body(ua)        
        message = res.get_message()
    else: 
        res.set_status(404)
        message = res.get_message()
    
    print(message) 
    conn.send(message)


if __name__ == "__main__":
    main()
