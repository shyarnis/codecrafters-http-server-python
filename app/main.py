import socket


def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    client_socket, client_address = server_socket.accept()

    request = client_socket.recv(1024).decode("utf-8")
    request_data = request.split("\r\n")

    if request_data[0].split(" ")[1] == "/":
        # ["GET", "/", "HTTP/1.1"]
        response = "HTTP/1.1 200 OK\r\n\r\n".encode()
    else:
        response = "HTTP/1.1 404 Not Found\r\n\r\n".encode()

    client_socket.send(response)
    client_socket.close()


if __name__ == "__main__":
    main()
