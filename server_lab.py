import socket
import threading
import time


class TupleSpaceServer:
    def __init__(self, port):
        self.port = port
        self.tuple_space = {}
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('localhost', self.port))
        self.server_socket.listen(5)
    def handle_client(self, client_socket):
        while True:
            try:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                length = int(data[:3])
                request = data[3:]
                operation, *args = request.split()
                if operation == 'R':
                    key = args[0]
                    if key in self.tuple_space:
                        response = f"{length:03d} OK ({key}, {self.tuple_space[key]}) read"
                    else:
                        response = f"{length:03d} ERR {key} does not exist"
                elif operation == 'G':
                    key = args[0]
                    if key in self.tuple_space:
                        value = self.tuple_space.pop(key)
                        response = f"{length:03d} OK ({key}, {value}) removed"
                    else:
                        response = f"{length:03d} ERR {key} does not exist"
                elif operation == 'P':
                    key, value = args
                    if len(key + value) > 970:
                        response = f"{length:03d} ERR key-value pair exceeds 970 characters"
                    else:
                        self.tuple_space[key] = value
                        response = f"{length:03d} OK ({key}, {value}) inserted"
                client_socket.send(response.encode('utf-8'))
            except Exception as e:
                print(f"Error handling client: {e}")
                break
        client_socket.close()

    def show_summary(self):
        while True:
            time.sleep(10)
            num_tuples = len(self.tuple_space)
            total_size = sum(len(key) + len(value) for key, value in self.tuple_space.items())
            if num_tuples > 0:
                avg_size = total_size / num_tuples
            else:
                avg_size = 0
            print(f"Summary: {num_tuples} tuples, average size: {avg_size} bytes")
    def start(self):
        summary_thread = threading.Thread(target=self.show_summary)
        summary_thread.daemon = True
        summary_thread.start()
        print(f"Server listening on port {self.port}")
        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Accepted connection from {client_address}")
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()