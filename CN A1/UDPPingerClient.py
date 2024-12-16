from socket import *
import time
import random

address = ("127.0.0.1", 12000) 

clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(1)

rtt=[]
lost=0
num_pings = 10
for i in range(num_pings):
    send_time=time.time()
    data = f'Ping {i+1} {send_time}'
    
    try:
        clientSocket.sendto(data.encode(), address)
        response, server = clientSocket.recvfrom(1024)
        print(f'Response: {response.decode()}')

        #NOTE: Can introduce artificial delay for better demonstration of RTT
        # artificial_delay = random.uniform(0.1, 0.9)
        # time.sleep(artificial_delay)

        recieve_time = time.time()
        rt = recieve_time - send_time
        rtt.append(rt)
        print(f'Ping {i+1} RTT : {rt} seconds')
    except timeout:
        lost+=1
        print(f'Ping {i+1} Request Timeout')
        

if(len(rtt)>0):
    mini=min(rtt)
    maxi=max(rtt)
    avg=sum(rtt)/len(rtt)
    print(f'Avgerage RTT : {avg} seconds')
    print(f'Maximum RTT : {maxi} seconds')
    print(f'Minimum RTT : {mini} seconds')
    
total_loss=(lost/num_pings)*100
print(f'Packet Loss Rate: {total_loss}%')