# UDPHeartbeatServer.py

import random
from socket import *
import time

# Create a UDP socket
# Use SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)

# Assign IP address and port number to socket
serverSocket.bind(('', 12000))

while True:
    # Generate random number in the range of 1 to 10
    rand = random.randint(1, 10) 
    
    # Receive the client packet along with the address it is coming from
    message, address = serverSocket.recvfrom(1024)

    # Extract the sequence number and timestamp from the client's message
    message = message.decode().split(' ')
    sequence_number = int(message[0])
    client_timestamp = float(message[1])

    # Introduce artificial delay for better demonstration
    # artificial_delay = random.uniform(0.1, 0.9)
    # time.sleep(artificial_delay)

    # Calculate the time difference
    server_timestamp = time.perf_counter()
    time_difference = server_timestamp - client_timestamp
    print(f'Sequence Number: {sequence_number}\nServer timestamp: {server_timestamp}\n Client timestamp: {client_timestamp}\n')
    message = f'{time_difference}'
    # If rand is less than 4, we consider the packet lost and do not respond (30% loss rate)
    if rand < 4:
        continue
    # Otherwise, the server responds
    serverSocket.sendto(message.encode(), address)
