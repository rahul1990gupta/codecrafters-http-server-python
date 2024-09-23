import socket  # noqa: F401


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
        req_parts = data.split(b"\r\n")
        print("Request Line", req_parts[0])
        url = req_parts[0].split(b" ")[1]
        if url == b"/":
            message = b"HTTP/1.1 200 OK\r\n\r\n"
        else: 
            message = b"HTTP/1.1 404 Not Found\r\n\r\n"
        conn.send(message)



if __name__ == "__main__":
    main()
