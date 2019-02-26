import socket
import sys
import time

file_size = sys.argv[1]
chunk_size = sys.argv[2]
protocol = sys.argv[3]

print("You want to create and send a file of " + file_size + " size")

if(file_size == "1GB"):
    with open('my_file', 'wb') as f:
        f.seek(1024 * 1024 * 1024) # One GB
        f.write(b'0')
elif(file_size == "500MB"):
    with open('my_file', 'wb') as f:
        f.seek(1024 * 1024 * 1024 // 2) # 500 MB
        f.write(b'0')

#---------------------------------------------------------------------------------
if (protocol == "TCP"):
    # Create a TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    with open('my_file', mode='rb') as file: # b -> binary
        fileContent = file.read()

    # Connect the socket to the port where the server is listening
    server_address = ('localhost', 10000)
    print('Connecting to %s port %s' % server_address)
    sock.connect(server_address)

    duration = 0

    try:
        file_length = len(fileContent)
        print("Sending %s size" % file_length)

        sock.send(chunk_size.encode())
        sock.sendall(fileContent)

    finally:
        print('Closing socket')
        sock.close()
#---------------------------------------------------------------------------------
elif (protocol == "UDP"):
    # Create an UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = ('localhost', 10000)

    sock.sendto(chunk_size.encode(), server_address)

    messages_sent = 0
    bytes_sent = 0
    with open('my_file', mode='rb') as file: # b -> binary
        while True:
            message = file.read(int(chunk_size))
            if len(message) == 0:
                sock.sendto(message, server_address)
                print("File sent size: " + str(bytes_sent))
                sys.exit()

            sock.sendto(message, server_address)
            messages_sent += 1
            bytes_sent += len(message)
            # print("Sending %s size" % file_length)
            # print("File was sent")

#---------------------------------------------------------------------------------
else:
    print("Protocol should be only TCP or UDP")