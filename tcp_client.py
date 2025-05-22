import socket

def send_message_to_server(message: str, server_host: str = 'localhost', server_port: int = 12345):
    client_socket = None
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (server_host, server_port)
        client_socket.connect(server_address)
        client_socket.sendall(message.encode())
        echoed_message_bytes = client_socket.recv(1024)
        echoed_message = echoed_message_bytes.decode()
        # The variable 'echoed_message' is now holding the server's response.
        # If this were a real application, it would be returned or used here.
    except socket.error as e:
        pass # Errors are silently ignored as per removal of print
    except Exception as e:
        pass # Errors are silently ignored
    finally:
        if client_socket:
            client_socket.close()

if __name__ == '__main__':
    test_message = "Hello, Server!"
    send_message_to_server(test_message)
    # The echoed message is received by send_message_to_server, but not printed or returned in this modified version.
