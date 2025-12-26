from socket import *
serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)

print('The server is ready to receive')
while True:
     connectionSocket, addr = serverSocket.accept()
     
     sentence = connectionSocket.recv(1024).decode()
     print(sentence)

     capitalizedSentence = sentence.upper()
     print(capitalizedSentence)

     connectionSocket.send(capitalizedSentence.encode())
     connectionSocket.close()

# http://10.128.131.51:12000/index.html I entered this into my browser and got cool stuff 
