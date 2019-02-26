import socket
import sys

protocol = sys.argv[1]

#---------------------------------------------------------------------------------
if (protocol == "TCP"):
    # Create a TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address = ('localhost', 10000)
    print('Starting up on %s port %s' % server_address)
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(1)

    # Amount of bytes received
    total_received = 0

    while True:
        # Wait for a connection
        print('Waiting for a connection')
        connection, client_address = sock.accept()
        try:
            print('Connection from', client_address)
            chunk_size = connection.recv(8)
            print("Will receive chunks of size: " + chunk_size.decode())
            # Receive the data in small chunks and retransmit it
            while True:
                data = connection.recv(int(chunk_size))
                if data:
                    total_received += len(data)
                else:
                    print('No more data from', client_address)
                    break
                #print('No more data from', client_address)
                
        finally:
            print("Received %s size" % total_received)
            total_received = 0
            # Clean up the connection
            connection.close()
#---------------------------------------------------------------------------------
elif (protocol == "UDP"):
    # Create an UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Amount of bytes received
    total_received = 0

    # Bind the socket to the port
    server_address = ('localhost', 10000)
    print('Starting up on %s port %s' % server_address)
    sock.bind(server_address)

    chunk_size, address = sock.recvfrom(8)
    print("Will receive chunks of size: " + chunk_size.decode())
    while True:
        data, address = sock.recvfrom(int(chunk_size))
        total_received += len(data)
        if(len(data) == 0):
            print("Received %s size" % total_received)
            total_received = 0
        #print('Received %s bytes from %s' % (len(data), address))

        # if data:
        #     total_received += len(data)
        # else:
        #     print('No more data to be received')
        #     print("Received %s size" % total_received)
        #     total_received = 0
#---------------------------------------------------------------------------------
else:
    print("Protocol should be only TCP or UDP")