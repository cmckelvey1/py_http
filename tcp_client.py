# tcp_client.py
# This script implements a simple TCP client that connects to a server,
# sends a message, receives the echoed message, and prints it.

import socket

def send_message_to_server(message: str, server_host: str = 'localhost', server_port: int = 12345):
    """
    Connects to the TCP server, sends a message, and prints the echoed response.

    Args:
        message (str): The message to send to the server.
        server_host (str): The hostname or IP address of the server.
        server_port (int): The port number of the server.
    """
    client_socket = None  # Initialize client_socket to None for the finally block
    try:
        # Create a TCP/IP socket
        # AF_INET specifies the address family (IPv4).
        # SOCK_STREAM specifies the socket type (TCP).
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Define the server address
        server_address = (server_host, server_port)
        print(f"Connecting to {server_address[0]} port {server_address[1]}...")

        # Connect the socket to the server's address and port
        client_socket.connect(server_address)
        print("Connected to server.")

        # Send the message to the server
        # The message needs to be encoded into bytes before sending.
        print(f"Sending message: '{message}'")
        client_socket.sendall(message.encode())

        # Receive the echoed message from the server
        # The argument (e.g., 1024) specifies the maximum amount of data to be received at once.
        echoed_message_bytes = client_socket.recv(1024)

        # Decode the received bytes back into a string (assuming UTF-8) and print it.
        echoed_message = echoed_message_bytes.decode()
        print(f"Received from server: '{echoed_message}'")

    except socket.error as e:
        # Handle socket-related errors (e.g., connection refused, host not found).
        print(f"Socket error: {e}")
    except Exception as e:
        # Handle other potential errors.
        print(f"An unexpected error occurred: {e}")
    finally:
        # This block executes whether an exception occurred or not.
        if client_socket:
            # Close the client socket to release resources.
            print("Closing client socket.")
            client_socket.close()

if __name__ == '__main__':
    # Define the test message to send to the server.
    test_message = "Hello, Server!"
    # Call the function to send the message and receive the echo.
    send_message_to_server(test_message)

    # Example of sending a different message
    # send_message_to_server("This is another test message.")

    # Example of trying to connect to a different port (likely to fail if server isn't there)
    # send_message_to_server("Testing connection failure", server_port=54321)
