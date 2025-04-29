import socket
import sys


def send_requests(server_host, server_port, request_file):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_host, server_port))

    try:
        with open(request_file, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(' ', 1)
                operation = parts[0]
                key = parts[1].split(' ', 1)[0]
                value = parts[1].split(' ', 1)[1] if len(parts) > 1 and operation == 'PUT' else ''
                message = f"{len(line):03d} {operation} {key}"
                if operation == 'PUT':
                    message += f" {value}"
                client_socket.send(message.encode())
                response = client_socket.recv(1024).decode()
                response_size = int(response[:3])
                response_content = response[3:].strip()
                print(f"{line}: {response_content}")
    except FileNotFoundError:
        print(f"Error: Request file '{request_file}' not found.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python client.py <server_host> <server_port> <request_file>")
        sys.exit(1)
    server_host = sys.argv[1]
    server_port = int(sys.argv[2])
    request_file = sys.argv[3]
    send_requests(server_host, server_port, request_file)