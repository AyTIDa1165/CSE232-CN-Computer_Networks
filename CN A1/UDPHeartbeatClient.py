from socket import *
import time

address = ("127.0.0.1", 12000) 

clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(1)

lost=0
miss = 0
seq_num = 0
while(miss < 3):
    seq_num += 1 
    client_timestamp = time.perf_counter()
    data = f'{seq_num} {client_timestamp}'
    
    try:
        clientSocket.sendto(data.encode(), address)
        response, server = clientSocket.recvfrom(1024)
        print(f'Time Difference: {response.decode()}')
        miss = 0
        #NOTE: For consecutive misses condition
    except timeout:
        miss += 1
        lost += 1
        print(f'Ping {seq_num} Request Timeout')
print(f"Program terminated after {seq_num} pings")
print(f'Packet Loss Rate: {lost*100/seq_num}%') 