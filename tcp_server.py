# tcp_server.py
# This script implements a simple TCP echo server that listens for incoming connections
# on localhost and a specified port. It echoes back any data received from a client.
# The server includes basic error handling for socket operations.

import socket

def start_server():
    server_socket = None  # Initialize server_socket to None to ensure it's defined in finally block
    try:
        # Create a TCP/IP socket object.
        # AF_INET specifies the address family (IPv4).
        # SOCK_STREAM specifies the socket type (TCP).
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Define the server address (host and port).
        # 'localhost' means the server will only be reachable from the same machine.
        # Port 12345 is arbitrarily chosen; ensure it's not in use by another application.
        server_address = ('localhost', 12345)
        print(f"Server starting up on {server_address[0]} port {server_address[1]}")

        # Bind the socket to the server address and port.
        # This associates the socket with the network interface and port number.
        server_socket.bind(server_address)

        # Enable the server to accept connections.
        # The argument (e.g., 1) specifies the maximum number of queued connections.
        server_socket.listen(1)
        print("Server listening on port 12345")

    except socket.error as e:
        # Handle socket-related errors that may occur during server setup
        # (e.g., address already in use, permission denied).
        print(f"Socket error during server setup: {e}")
        if server_socket:
            server_socket.close() # Attempt to close the socket if it was created
        return  # Exit the function if server setup fails

    # Main server loop to continuously accept connections.
    try:
        while True:
            client_socket = None  # Initialize client_socket for each new connection attempt
            try:
                # Wait for an incoming connection.
                # This call blocks until a client connects.
                # Returns a new socket object for the client and the client's address.
                print("Waiting for a connection...")
                client_socket, client_address = server_socket.accept()
                print(f"Connection from {client_address}")

                # Inner loop to handle communication with the connected client.
                while True:
                    try:
                        # Receive data from the client (up to 1024 bytes).
                        # This call blocks until data is received or the client closes the connection.
                        data = client_socket.recv(1024)
                        if data:
                            # If data is received, decode it (assuming UTF-8) and print it.
                            print(f"Received: {data.decode()}")
                            # Echo the received data back to the client.
                            print("Echoing data back to client")
                            client_socket.sendall(data)
                        else:
                            # If recv returns an empty byte string, the client has closed the connection.
                            print("Client sent no data, closing client connection.")
                            break # Exit the inner loop to close this client's socket.
                    except socket.error as e:
                        # Handle socket errors during data reception or sending (e.g., connection reset).
                        print(f"Socket error during client communication: {e}")
                        break  # Exit the inner loop to close this client's socket.
                    except UnicodeDecodeError as e:
                        # Handle errors if the received data is not valid UTF-8.
                        print(f"Unicode decode error: {e}. Client might have sent non-UTF-8 data.")
                        # For this simple server, we break. A more robust server might send an error
                        # message to the client or try to handle the data differently.
                        break


            except socket.error as e:
                # Handle errors that might occur during the accept() call.
                # For example, the listening socket might have been closed unexpectedly.
                print(f"Socket error during accept: {e}")
                # If a client socket was somehow created before the error, ensure it's closed.
                if client_socket:
                    client_socket.close()
                # Continue to the next iteration of the outer loop to try accepting new connections.
                # Depending on the error, one might choose to break the outer loop instead.
                continue

            finally:
                # This block executes whether the client communication loop finished normally or due to an exception.
                if client_socket:
                    print("Closing client socket")
                    try:
                        # Close the client socket to release resources.
                        client_socket.close()
                    except socket.error as e:
                        # Handle potential errors during client socket closure.
                        print(f"Socket error while closing client socket: {e}")


    except KeyboardInterrupt:
        # Handle a KeyboardInterrupt (Ctrl+C) to gracefully shut down the server.
        print("Server is shutting down due to KeyboardInterrupt.")
    finally:
        # This block executes whether the main server loop exited normally or due to an exception (like KeyboardInterrupt).
        if server_socket:
            print("Closing server socket")
            try:
                # Close the server socket to release the listening port.
                server_socket.close()
            except socket.error as e:
                # Handle potential errors during server socket closure.
                print(f"Socket error while closing server socket: {e}")

if __name__ == '__main__':
    # If the script is executed directly, start the server.
    start_server()
