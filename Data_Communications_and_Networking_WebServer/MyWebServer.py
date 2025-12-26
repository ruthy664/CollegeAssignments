import socket
import sys
import threading
from datetime import datetime
import os

serverPort = 12000 #8888
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def respond(connectionSocket, address):
    request = connectionSocket.recv(1024).decode()
    print('(Server) <======= request ========= (Client)')

    ###### Fill in Start ######
    lines = request.split("\r\n")
    for line in lines:
        print(line)
    
    line1 = lines[0].split()
    method = line1[0]
    req_file = line1[1].lstrip('/')
    send = False
    content_length = 0

    try:
        file = open(req_file,'r')
        last_modi = os.path.getmtime(req_file)
        last_modified = datetime.fromtimestamp(last_modi)
        content_length = os.path.getsize(req_file)
        modified_since = None
        if (method == "GET"): 
            print("(Server) ======== response ========> (Client)")
            # conditional get
            modified_header = False
            for line in lines:
                if line.lower().startswith('if-modified-since:'):
                    ms = line.split(':', 1)[1].strip()
                    modified_since = datetime.strptime(ms, "%m/%d/%Y %H:%M:%S")
                    break
            if modified_since and last_modified <= modified_since:
                response = 'HTTP/1.1 304 Not Modified\r\n'
            else:
                response = 'HTTP/1.1 200 OK\r\n'
                send = True
                contents = file.read()
        elif (method == "HEAD"): 
            response = 'HTTP/1.1 200 OK\r\n'
        else: 
            print("(Server) ======== response ========> (Client)")
            response = 'HTTP/1.1 501 Not Implemented\r\n'
        file.close()
    except FileNotFoundError:
        print('(Server) ======== response ========> (Client)')
        response = 'HTTP/1.1 404 Not Found\r\n'

    status_code = response.split()[1] 
    # headers: 
    date = datetime.now()
    response += 'Date: ' + date.strftime('%m/%d/%Y %H:%M:%S') + '\r\n'
    if status_code == '200':
        response += 'Connection: keep-alive\r\n'
    response += 'Server: localhost\r\n'
    if status_code == '200':
        response += 'Last-Modified: ' + str(last_modified.strftime('%m/%d/%Y %H:%M:%S')) + '\r\n'
    response += 'Content-Length: ' + str(content_length) + '\r\n\r\n'
    print(response) 

    connectionSocket.send(response.encode())
    if send == True:
        connectionSocket.send(contents.encode())
    connectionSocket.close()
    ###### Fill in End ######

    return

# start the web server
try:
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSocket.bind(('', serverPort))
    print("The server is ready to receive on port {port}.\n".format(port=serverPort))
except Exception as e:
    print("An error occurred on port {port}\n".format(port=serverPort))
    serverSocket.close()
    sys.exit(1)

serverSocket.listen(1)

# handle requests
while True:
    (connectionSocket, address) = serverSocket.accept()
    print("Received connection from {addr}\n".format(addr=address))
    threading.Thread(target=respond, args=(connectionSocket, address)).start()
