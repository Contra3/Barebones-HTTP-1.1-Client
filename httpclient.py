# Ronny Recinos

import logging
import socket
import sys
import ssl


# Notes:
# You may assume that the URL will not include a fragment, query string, or authentication credentials.
# You are not required to follow any redirects - #only return bytes when receiving a 200 OK response from the server#.
# ✔ If for any reason your program cannot retrieve the resource correctly, retrieve_url should return None.

def retrieve_url(url):

    #Demlimiter ':' used to split http
    parsedHttp = url.split(':')
    parsedHttp = parsedHttp[0]
    # print(parsedHttp[0])

    # Check parsed http and handle the port depending on what it is
    if parsedHttp == 'http':
        port = 80
    elif parsedHttp == 'https':
        port = 443
    else:
        return None
    
    # Using the delimiter / to get the Host name for the GET method
    parsedHostName = url.split('/', 3)
    parsedHostName = parsedHostName[2]
    #print(parsedHostName)

    portInHostName = parsedHostName.split(':', 1)
    #print(portInHostName)

    try:
        parsedHostName = portInHostName[0]
        port =  int(portInHostName[1])
    except IndexError:
        parsedHostName = portInHostName[0]

    # Using the delimiter / to get the path name for the GET method
    parsedPathName = url.split('/', 3)

    #print(parsedHostName)
    #print(port)

    try:
        parsedPathName = '/' + parsedPathName[3]
    except IndexError:
        parsedPathName = '/'
     
    #print(parsedPathName)

    # Getting the ip address of the host name
    try:
        host_ip = socket.getaddrinfo(parsedHostName, port)[0][4][0]
    except:
        return None

    # Construct the GET method using the information above
    constructGET = b"GET " + parsedPathName.encode('utf-8') + b" HTTP/1.1\r\nHost: " + parsedHostName.encode('utf-8') + b"\r\nAccept: */*\r\n\r\n" 


    # Open a socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host_ip, port))
    except:
        return None

    # Using SSL to wrap the socket
    if port == 443:
        try:
            s = ssl.wrap_socket(s, cert_reqs=ssl.CERT_REQUIRED, ca_certs='cacert.pem')
        except:
            return None

    s.sendall(constructGET)

    headerBuffer = ''
    chunked = False
    okResponse = False
    expectedContentLength = 0

    # Processes the Header response from the server
    while True:
        
        if (headerBuffer.find('\r\n\r\n') != -1): # End of Header we break from loop
            break

        msg = s.recv(1) # Get a byte of data each loop
        headerBuffer += msg.decode('utf-8') # Build a string with the data to be able to parse it correctly

        # If the data is chunked, we catch it here
        if (headerBuffer.find('chunked') != -1): 
            chunked = True

        # If it response contain 200 OK then set okResponse to true
        if (headerBuffer.find('HTTP/1.1 200 OK') != -1):
            okResponse = True
    
    if okResponse == False:
        return None
        
    for headerLine in headerBuffer.splitlines():
        # Grab the content-length from the header
        if (headerLine.find('Content-Length:') != -1):
            expectedContentLength = int(headerLine.split('Content-Length: ', 1)[1])
        
    contentRecieved = 0
    bodyBuffer = b''
    chunks = b''
    newChunk = b''

    if chunked:

        while True:
            if (chunks.find(b'\r\n\r\n') != -1): # Check for carriage return of chunked body
                break
            msg = s.recv(1) # Get 1024 bytes of data each loop
            chunks += msg

        newChunk = b""

        while True:

            # Separate the leading hex and the chunk body
            chunkSizeAndChunkBody = chunks.split(b"\r\n", 1)

            # Grabbing the hex number that notifies the size of the current chunk will be
            chunkSizeHexNum = chunkSizeAndChunkBody[0]

            # Checking if we hit the end of line
            if chunkSizeHexNum == b'0':
                break

            # Convert the hex number into an integer to help traverse through the byte string chunk
            chunkSize = int(chunkSizeHexNum, 16)

            # Chunk will have the rest of the chunkbody for processing the chunk
            chunk = chunkSizeAndChunkBody[1]

            # Strip the nonessential data of the chunk based on the ChunkSize
            newChunk += chunk[:chunkSize]
            
            # Our chunks will be updated to remove the leftover chunks that have already been read
            chunks = chunk[chunkSize+2:]
        
        s.close() # Closing the socket
        return newChunk
    else:
        while contentRecieved < expectedContentLength: # Grabs all the expected data from the server
            msg = s.recv(1024) # Grab 1024 bytes each call
            bodyBuffer += msg # Construct the bodyBuffer that will hold the server data
            contentRecieved += len(msg) # Increment the contentRecieved based on the length of the msg that was recieved
        
        s.close()  # Closing the socket

        #print(bodyBuffer.decode())
        return bodyBuffer

    return None
    
# sys.stdout.buffer.write(retrieve_url(sys.argv[1]))



#print retrieve_url('http://www.example.com')
