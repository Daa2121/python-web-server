#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
A simple Web server.
GET requests must name a specific file,
since it does not assume an index.html.
"""

import socket
import threading


def handler(conn_socket: socket.socket, address: tuple[str, int]) -> None:
    """
    Handles the part of the client work-flow that is client-dependent,
    and thus may be delayed by the user, blocking program flow.
    """
    try:
        # Receives the request message from the client
        request_message = conn_socket.recv(1024).decode()

        # Extract the path of the requested object from the message
        # The path is the second part of HTTP header, identified by [1]
        request_path = request_message.split(" ")[1][1:]

        # Because the extracted path of the HTTP request includes
        # a character '\', we read the path from the second character
        # Read file off disk, to send
        # Store the content of the requested file in a temporary buffer
        with open(request_path, "rb") as file:
            file_content = file.read()

        # Send the HTTP response header line to the connection socket
        response_header = "HTTP/1.1 200 OK\r\n\r\n"
        conn_socket.send(response_header.encode())

        # Send the content of the requested file to the connection socket
        conn_socket.send(file_content)

    except IOError:
        # Send HTTP response message for file not found (404)
        error_response = "HTTP/1.1 404 Not Found\r\n\r\n"
        conn_socket.send(error_response.encode())

        # Open file, store the content of the requested file in a temporary buffer (variable).
        with open("web_files/not_found.html", "rb") as file:
            file_content = file.read()
            # Send the content of the requested file to the connection socket
            conn_socket.send(file_content)

    except:
        print("Bad request")
    finally:
        conn_socket.close()


def main() -> None:
    server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    server_port = 6789
    # Bind the socket to server address and server port
    server_socket.bind(("", server_port))

    # Listen to at most 2 connection at a time
    # Server should be up and running and listening to the incoming connections
    server_socket.listen(2)
    threads = []
    try:
        while True:
            # Set up a new connection from the client
            conn_socket, address = server_socket.accept()

            # call handler here, start any threads needed
            new_thread = threading.Thread(target=handler, args=(conn_socket, address))
            new_thread.start()

            # Just to keep track of threads
            threads.append(new_thread)
    except Exception as e:
        print("Exception occured (maybe you killed the server)")
        print(e)
    except:
        print("Exception occured (maybe you killed the server)")
    finally:
        server_socket.close()


if __name__ == "__main__":
    main()
