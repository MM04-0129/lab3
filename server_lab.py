import socket
import threading
import time


class TupleSpace:
    def __init__(self):
        self.tuples = {}
        self.stats = {
            'tuple_count': 0,
            'average_tuple_size': 0,
            'average_key_size': 0,
            'average_value_size': 0,
            'total_clients': 0,
            'total_operations': 0,
            'total_READs': 0,
            'total_GETs': 0,
            'total_PUTs': 0,
            'total_errors': 0
        }
        self.lock = threading.Lock()
def read(self, key):
        with self.lock:
            if key in self.tuples:
                self.stats['total_READs'] += 1
                self.stats['total_operations'] += 1
                return f"OK ({key}, {self.tuples[key]}) read"
            else:
                self.stats['total_errors'] += 1
                self.stats['total_operations'] += 1
                return f"ERR {key} does not exist"
def get(self, key):
        with self.lock:
            if key in self.tuples:
                value = self.tuples.pop(key)
                self.stats['tuple_count'] -= 1
                self.stats['total_GETs'] += 1
                self.stats['total_operations'] += 1
                return f"OK ({key}, {value}) removed"
            else:
                self.stats['total_errors'] += 1
                self.stats['total_operations'] += 1
                return f"ERR {key} does not exist"
def put(self, key, value):
        with self.lock:
            if key in self.tuples:
                self.stats['total_errors'] += 1
                self.stats['total_operations'] += 1
                return f"ERR {key} already exists"
            else:
                self.tuples[key] = value
                self.stats['tuple_count'] += 1
                self.stats['total_PUTs'] += 1
                self.stats['total_operations'] += 1
                return f"OK ({key}, {value}) added"
def update_stats(self):
        while True:
            time.sleep(10)
            with self.lock:
                if self.stats['tuple_count'] > 0:
                    total_tuple_size = sum(len(key) + len(value) for key, value in self.tuples.items())
                    total_key_size = sum(len(key) for key in self.tuples.keys())
                    total_value_size = sum(len(value) for value in self.tuples.values())
                    self.stats['average_tuple_size'] = total_tuple_size / self.stats['tuple_count']
                    self.stats['average_key_size'] = total_key_size / self.stats['tuple_count']
                    self.stats['average_value_size'] = total_value_size / self.stats['tuple_count']
                print(f"Tuple Space Summary: "
                      f"Tuple Count: {self.stats['tuple_count']}, "
                      f"Average Tuple Size: {self.stats['average_tuple_size']}, "
                      f"Average Key Size: {self.stats['average_key_size']}, "
                      f"Average Value Size: {self.stats['average_value_size']}, "
                      f"Total Clients: {self.stats['total_clients']}, "
                      f"Total Operations: {self.stats['total_operations']}, "
                      f"Total READs: {self.stats['total_READs']}, "
                      f"Total GETs: {self.stats['total_GETs']}, "
                      f"Total PUTs: {self.stats['total_PUTs']}, "
                      f"Total Errors: {self.stats['total_errors']}")


def handle_client(client_socket, client_address, tuple_space):
    tuple_space.stats['total_clients'] += 1
    try:
        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            command = data[:3]
            operation = data[3]
            key = data[4:].split(' ', 1)[0]
            value = data[4:].split(' ', 1)[1] if operation == 'P' else ''
            if operation == 'R':
                response = tuple_space.read(key)
            elif operation == 'G':
                response = tuple_space.get(key)
            elif operation == 'P':
                response = tuple_space.put(key, value)
            else:
                response = "ERR invalid operation"
                tuple_space.stats['total_errors'] += 1
                tuple_space.stats['total_operations'] += 1
            response_msg = f"{len(response):03d} {response}"
            client_socket.send(response_msg.encode())
    except Exception as e:
        print(f"Error handling client {client_address}: {e}")
    finally:
        client_socket.close()
def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', port))
    server_socket.listen(5)
    print(f"Server is running on port {port}")

    tuple_space = TupleSpace()
    stats_thread = threading.Thread(target=tuple_space.update_stats)
    stats_thread.daemon = True
    stats_thread.start()

    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address, tuple_space))
        client_thread.start()


if __name__ == "__main__":
    start_server(51234)
