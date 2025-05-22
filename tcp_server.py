import socket

def start_server():
    server_socket = None
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 12345)
        server_socket.bind(server_address)
        server_socket.listen(1)
    except socket.error as e:
        if server_socket:
            server_socket.close()
        return

    try:
        while True:
            client_socket = None
            try:
                client_socket, client_address = server_socket.accept()
                while True:
                    try:
                        data = client_socket.recv(1024)
                        if data:
                            client_socket.sendall(data)
                        else:
                            break
                    except socket.error as e:
                        break
                    except UnicodeDecodeError as e:
                        break
            except socket.error as e:
                if client_socket:
                    client_socket.close()
                continue
            finally:
                if client_socket:
                    try:
                        client_socket.close()
                    except socket.error as e:
                        pass
    except KeyboardInterrupt:
        pass
    finally:
        if server_socket:
            try:
                server_socket.close()
            except socket.error as e:
                pass

if __name__ == '__main__':
    start_server()
