import socket


def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    client_socket, client_address = server_socket.accept()

    request = client_socket.recv(1024).decode("utf-8")
    request_data = request.split("\r\n")
    path = request_data[0].split(" ")[1]

    if path == "/":
        response = "HTTP/1.1 200 OK\r\n\r\n".encode()

    elif path.startswith("/echo/"):
        string: str = path.split("/")[-1]
        # ['', 'echo', 'hello']
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(string)}\r\n\r\n{string}".encode()

    else:
        response = "HTTP/1.1 404 Not Found\r\n\r\n".encode()

    client_socket.send(response)
    client_socket.close()


if __name__ == "__main__":
    main()
