import socket  # noqa: F401


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    conn, address = server_socket.accept() # wait for client

    # data = server_socket.recv(48)
    message = b"HTTP/1.1 200 OK\r\n\r\n"
    conn.send(message)



if __name__ == "__main__":
    main()
