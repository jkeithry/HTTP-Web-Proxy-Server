#!python2
import socket
if len(sys.argv) <= 1:

    print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
    sys.exit(2)

# Create a server socket, bind it to a port and start listening

tcpSerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Fill in start.
recv_buffer = 4096
TCP_IP = '127.0.0.1'
TCP_PORT = 8888
tcpSerSock.bind((TCP_IP, TCP_PORT))
tcpSerSock.listen(2)

# Fill in end.


while 1:


    # Strat receiving data from the client
    print('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)
    message_raw = tcpCliSock.recv(1024)
    message = message_raw.decode()
    print("message:", message)
    if message == '':
        continue
    # Extract the filename from the given message
    print("message.split()[1]:", message.split()[1])
    filename = message.split()[1].partition("/")[2]
    print("filename:", filename)
    fileExist = "false"
    filetouse = "/" + filename
    print("filetouse:", filetouse)

    try:
        # Check whether the file exist in the cache
        f = open( filetouse[1:], "rb")
        outputdata = f.read()
        fileExist = "true"

        # ProxyServer finds a cache hit and generates a response message
        tcpCliSock.send("HTTP/1.1 200 OK\r\n".encode())
        tcpCliSock.send("Content-Type:text/html\r\n".encode())

        # Fill in start.

        tcpCliSock.send(outputdata)

        # Fill in end.
        f.close()
        print('Read from cache')

    # Error handling for file not found in cache
    except IOError:
        if fileExist == "false":

            # Create a socket on the proxyserver

            c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            hostname = filename.replace("www.","",1)
            try:
                # Connect to the socket to port 80
                # Fill in start.
                c.connect((hostname,80))
                # Fill in end.

                # Create a temporary file on this socket and ask port 80
                # for the file requested by the client
                fileobj = c.makefile('rwb', 0)
                fileobj.write(b'GET / HTTP/1.0\r\n\r\n')
                # Read the response into buffer
                # Fill in start.
                buff = fileobj.read()



                # Fill in end.

                # Create a new file in the cache for the requested file.
                # Also send the response in the buffer to client socket
                # and the corresponding file in the cache
                tmpFile = open("./" + filename,"wb")
                tmpFile.write(buff)
                tcpCliSock.send("HTTP/1.1 200 OK\r\n".encode())
                tcpCliSock.send("Content-Type:text/html\r\n".encode())
                for i in range(0, len(buff)):
                    tcpCliSock.send(buff)



                # Fill in end.
                print('sent to client')

            except IOError:
                print("Illegal request")
        else:
            # HTTP response message for file not found
            # Fill in start.
            header = 'HTTP/1.1 404 Not Found\n\n'
            response = '<html>' \
                       '    <h1>' \
                       '        Error   ' \
                       '        404: File' \
                       '        not found  ' \
                       '     </h1>' \
                       '</html>'
            tcpCliSock.send(header.encode() + response.encode())
            # Fill in end.
            # Close the client and the server sockets

            tcpCliSock.close()

    # Fill in start.
tcpSerSock.close()
    # Fill in end.
