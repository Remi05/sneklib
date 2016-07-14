#Author: Remi Pelletier
#File:   tcp_server.py
#Desc.:  A small application using my TcpServer from rp_tcp.py .

import sys
import socket
import rp_tcp


#Get the host info
host = socket.gethostbyname(socket.gethostname())

#Select a port.
port = 8080

#Create a server.
server = rp_tcp.TcpServer(host, port)

#Initialize the server.
try:
    server.initialize()
except Exception as e:
    print("Could not create server.")
    print("Error message : " + str(e))
    sys.exit(1)

print("Server setup at " + host + ":" + str(port))

#Accept client connections.
while True:
    print("Waiting for a connection...")
    server.accept() #Accept the connection.
    print("Client connected : " + server.current_client_address[0])
    server.send("Hello!".encode('utf-8')) #Respond to the client.
    server.close() #Close the connection.



