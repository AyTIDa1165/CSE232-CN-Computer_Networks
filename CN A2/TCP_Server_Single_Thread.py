#import socket module
from socket import *
import threading
import sys # In order to terminate the program

serverSocket = socket(AF_INET, SOCK_STREAM)
#Prepare a sever socket

#Fill in start
serverSocket.bind(('', 6789))
serverSocket.listen(1)
#Fill in end

while True:
    thread_id = threading.get_ident()  # Get the current thread ID
    print(f'Thread ID: {thread_id} is handling the request.')
    #Establish the connection
    print('Ready to serve...')
    #Fill in start
    connectionSocket, addr = serverSocket.accept()  
    #Fill in end
    try:
        #Fill in start
        message = connectionSocket.recv(1024).decode()
        #Fill in end
        if not message:
            continue
        filename = message.split()[1]    
        print(f'Client is requesting {filename[1:]}')    
        f = open(filename[1:])  # Skip the first character (which is a '/')
        outputdata = f.read()  # Fill in start #Fill in end
        f.close()  # Close the file after reading
        #Send one HTTP header line into socket
        #Fill in start
        header = 'HTTP/1.1 200 OK\r\n'
        content_type = 'Content-Type: text/html\r\n'
        connectionSocket.send(header.encode())
        connectionSocket.send(content_type.encode())
        connectionSocket.send('\r\n'.encode())
        #Fill in end

        #Send the content of the requested file to the client
        # connectionSocket.send(outputdata.encode())
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send('\r\n'.encode())
        connectionSocket.close()

    except IOError:
        header = 'HTTP/1.1 404 Not Found\r\n\r\n'
        response = '<html><body><h1>404 Not Found</h1></body></html>'
        connectionSocket.send(header.encode())
        connectionSocket.send(response.encode())
        print('404 Not Found')
        #Fill in end

        #Close client socket
        #Fill in start
        connectionSocket.close()
        #Fill in end
    
serverSocket.close()
sys.exit() #Terminate the program after sending the corresponding data