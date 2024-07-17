import socket
import threading
import sys
import os


def client_request(client_socket):
    request = client_socket.recv(1024).decode("utf-8")
    request_data = request.split("\r\n")
    path = request_data[0].split(" ")[1]
    body = request_data[-1]
    request_method = request_data[0].split(" ")[0]

    if request_method == "GET":
        response = get_request_method(path, request_data)

    if request_method == "POST":
        response = post_request_method(path, body)

    client_socket.send(response)
    client_socket.close()


def get_request_method(path, request_data):
    if path == "/":
        return f"HTTP/1.1 200 OK\r\n\r\n".encode()

    elif path.startswith("/echo/"):
        string: str = path.split("/")[-1]
        # ['', 'echo', 'hello']
        return f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(string)}\r\n\r\n{string}".encode()

    elif path.startswith("/user-agent"):
        user_agent = request_data[2].split(": ")[1]
        # ['GET /user-agent HTTP/1.1', 'Host: localhost:4221', 'Accept: */*', 'User-Agent: foobar/1.2.3', '', '']
        # ['Accept', '*/*']
        # */*
        return f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(user_agent)}\r\n\r\n{user_agent}".encode()

    elif path.startswith("/files"):
        directory = sys.argv[2]
        filename = path.split("/")[-1]

        try:
            with open(f"/{directory}/{filename}", "r") as file:
                response_body = file.read()
                return f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(response_body)}\r\n\r\n{response_body}".encode()

        except FileNotFoundError as e:
            return f"HTTP/1.1 404 Not Found\r\n\r\n".encode()

    else:
        return "HTTP/1.1 404 Not Found\r\n\r\n".encode()

    return


def post_request_method(path, body):
    if path.startswith("/files"):
        directory = sys.argv[2]
        filename = path.split("/")[-1]
        file_path = os.path.join(directory, filename)

        try:
            # with open(f"/{directory}/{filename}", "w") as file:
            with open(file_path, "w") as file:
                file.write(body)
                return f"HTTP/1.1 201 Created\r\n\r\n".encode()

        except FileNotFoundError as e:
            return f"HTTP/1.1 404 Not Found\r\n\r\n".encode()

    return


def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    while True:
        client_socket, client_address = server_socket.accept()

        client_handler = threading.Thread(target=client_request, args=(client_socket,))
        client_handler.start()


if __name__ == "__main__":
    main()
