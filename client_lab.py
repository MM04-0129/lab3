import socket
import sys


def send_request(client_socket, request):
    # Calculate the total length of the request message
    length = len(request) + 3
    full_request = f"{length:03d} {request}"
    # Send the request to the server
    client_socket.send(full_request.encode('utf-8'))
    # Receive the response from the server
    response = client_socket.recv(1024).decode('utf-8')
    print(f"Request: {request}, Response: {response}")


def main():
    if len(sys.argv) != 4:
        print("Usage: python tuple_space_client.py <host> <port> <request_file>")
        sys.exit(1)
    host = sys.argv[1]
    port = int(sys.argv[2])
    request_file = sys.argv[3]
    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Connect to the server
        client_socket.connect((host, port))
        with open(request_file, 'r') as file:
            for line in file:
                request = line.strip()
                # Send each request to the server
                send_request(client_socket, request)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the socket
        client_socket.close()


if __name__ == "__main__":
    main()