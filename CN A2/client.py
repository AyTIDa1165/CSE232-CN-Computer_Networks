import sys
from socket import *

#CMD INSTRUCTION: python client.py 192.168.1.19 6789 HelloWorld.html

if len(sys.argv) < 4:
    print("Incorrect input")
    print("Usage: python client.py <server_host> <server_port> <filename>")
    sys.exit(1)

server_host = sys.argv[1]
server_port = sys.argv[2]
try:
    server_port = int(server_port)
except ValueError:
    print(f"Error: Port '{server_port}' is not a valid integer.")
    sys.exit(1)
filename = sys.argv[3]

# print(server_host, server_port, filename)

clientsocket=socket(AF_INET, SOCK_STREAM)
try:
    clientsocket.connect((server_host, server_port))
    http_request = f"GET /{filename} HTTP/1.1\r\nHost: {server_host}\r\nConnection: close\r\n\r\n"
    clientsocket.send(http_request.encode())
    response = b""
    while True:
        data = clientsocket.recv(4096)
        if not data:
            break
        response += data
    print(response.decode())
except Exception as e:
    print("unable to connect")
    sys.exit()
finally:
    clientsocket.close()