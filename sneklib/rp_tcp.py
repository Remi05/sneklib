#Author: Remi Pelletier
#File:   rp_tcp.py
#Desc.:  A module containing a very basic TCP client and server 
#        (based on the examples provided at : https://docs.python.org/3.0/library/socket.html).

import socket


class SocketCreationError(Exception):
    pass

class SocketBindingError(Exception):
    pass

class SocketConnectionError(Exception):
    pass


#Creates a TCP/IP socket compatible with IPV4 and IPV6.
#Returns a tuple containing a socket instance and the associated address
#if it was created successfully or a tuple containing (None,None) otherwise. 
def _create_socket(host, port):
    sckt = None
    for result in socket.getaddrinfo(host, port, socket.AF_UNSPEC, socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
        family, socket_type, protocol, canon_name, socket_address = result
        try:
            sckt = socket.socket(family, socket_type, protocol) #Create the socket.
        except socket.error as e: #Error while creating the socket.
            sckt = None
            continue
        break
    return sckt, None if sckt is None else socket_address


#A very basic TCP server implementation.
class TcpServer:
    def __init__(self, host = None, port = None):
         self.host = host if host is not None else socket.gethostbyname(socket.gethostname())
         self.port = port
         self.socket = None
         self.current_connection = None
         self.current_client_address = None
         
    #Creates the TCP/IP socket and initializes it.
    def initialize(self):
        self.socket, self.socket_address = _create_socket(self.host, self.port) #Create the socket
        if self.socket is None:
            raise SocketCreationError("An error occured when creating the socket.")
        try:
            self.socket.bind(self.socket_address) #Bind the socket to the address.
            self.socket.listen() #Setup the socket to accept connections.
        except socket.error as e:
            self.shutdown()
            raise SocketBindingError("An error occured when binding the socket.")

    #Closes and destroys the TCP/IP socket (also closes the
    #connection with currently connected client if there is one).
    def shutdown(self):
        if self.socket is not None:
            if self.current_connection is not None:
                self.close()
            self.socket.close()
            self.socket = None

    #Waits for a client to connect (stalling function).
    def accept(self):
        if self.socket is not None:
            self.current_connection, self.current_client_address = self.socket.accept()
    
    #Sends the given data to the currently connected client.
    def send(self, data):
        if self.current_connection is not None:
            self.current_connection.send(data)
               
    #Waits for the currenly connected client to send data and returns it.      
    def receive(self, buffer_size = 256):
        data = None
        if self.current_connection is not None:
             data = self.current_connection.recv(buffer_size)
        return data

    #Closes the connection with the currently connected client.
    def close(self):
        if self.current_connection is not None:
            self.current_connection.close()
            self.current_connection = None
            self.current_client_address = None


#A very basic TCP client implementation.
class TcpClient:   
    def __init__(self):
        self.socket = None
        self.remote_host = None
        self.port = None

    #Creates the TCP/IP socket and connects to 
    #the server at the given remote host.
    def connect(self, host, port):
        self.remote_host = host
        self.port = port
        self.socket, self.socket_address = _create_socket(self.remote_host, self.port) #Create the socket.
        if self.socket is None:
            raise SocketCreationError("An error occured when creating the socket.")
        try:
            self.socket.connect(self.socket_address) #Connect to the server.
        except socket.error as e:
            self.close()
            raise SocketConnectionError("An error occured when trying to connect to the remote host.")

    #Sends the given data to the currently connected server.
    def send(self):
        if self.socket is not None:
            self.socket.send(data)

    #Waits for the currenly connected server to send data and returns it. 
    def receive(self, buffer_size = 256):
        data = None
        if self.socket is not None:
             data = self.socket.recv(buffer_size)
        return data

    #Closes the connection with the currently connected server.
    def close(self):
        if self.socket is not None:
            self.socket.close()
            self.socket = None
            self.socket_address = None
            self.remote_host = None
            self.port = None
    

