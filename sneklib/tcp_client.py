#Author: Remi Pelletier
#File:   tcp_client.py
#Desc.:  A small application using my TcpClient from rp_tcp.py .

import sys
import socket
import rp_tcp

#Read the host from the console.
print("Host: ")
host = input()

#Read the port from the console.
print("Port: ")
port = int(input())

#Create a client.
client = rp_tcp.TcpClient()

#Connect to the server.
try:
    client.connect(host, port)
except Exception as e:
    print("Could not connect to server at " + host + ":" + str(port))
    print("Error message : " + str(e))
    sys.exit(1)

#Wait for response.
print("Connection established. Waiting for server response...")
while True:
    data = client.receive()
    if data:
        print(data)
    else:
        break
    
#Close the connection.
client.close()
