# this is the server for the Fall 2022 CS 371 Project

import socket, threading, _thread as thread, os
from FileClass import File
print_lock = threading.Lock()

FORMAT = 'utf-8'

numClients = 0
numThreads = 0
clients = []
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if not os.path.exists("./ServerFiles"):
  os.mkdir("./ServerFiles")


HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65322  # Port to listen on (non-privileged ports are > 1023)
fileStorage = {}

def Upload(fileName, connection):
  
  CreateFile(fileName)
  fileStorage[fileName] = File(fileName)
  fileObj = fileStorage[fileName]
  
  fileBytes = connection.recv(1024)
  fileObj.fileContents = fileBytes
  
  print(f"""
  {fileObj.name}
  {fileObj.path}
  {fileObj.fileSize}
  {fileObj.downloads}
  {fileObj.fileContents}
  """)
  
def Download(fileName, connection):
  existsOnServer, fileBytes = GetFile(fileName)
  fileObj = fileStorage[fileName]

  connection.sendall(fileBytes)
  
  fileStorage[fileName].downloads += 1
  
  print(f"""
  {fileObj.name}
  {fileObj.path}
  {fileObj.fileSize}
  {fileObj.downloads}
  {fileObj.fileContents}
  """)

  
  ackData = connection.recv(1024)
  ackData = ackData.decode(FORMAT)
  if ackData == "ACK":
    if not existsOnServer:
      if os.path.isfile(fileName):
        os.remove(fileName)
      else:
        print("ERROR: file does not exist\n")
  else:
    print("ERROR: no ack from client\n")
    
  
def HandleClient(connection):
  # initalize the client and give the client an ID
  global numThreads
  clientID = str(numClients)
  print(f"I am handling a client in thread {numThreads}")

  while True:
    # wait for the client to send a command
    data = connection.recv(1024)
    data = data.decode(FORMAT)

    
    command, fileName = data.split()
    
    if command == "UPLOAD":
      Upload(fileName, connection)

    
    elif command == "DOWNLOAD":
      Download(fileName, connection)
      
      
    elif data.decode(FORMAT) == "DISCONNECT":
      temp = "GoodBye"
      connection.send(temp.encode(FORMAT))
      connection.close()
      break
  


def GetFile(fileName):
  existsOnServer = True

  fileStorage[fileName] = File(fileName)
  fileObj = fileStorage[fileName]
  
  if not os.path.exists(f"./ServerFiles/{fileName}"):
    existsOnServer = False
    # we need to check if the other client has it... 
    # make fileObj.fileContents = to client 2's file
    # fileObj.size = size of client 2's file
    
    fileObj.fileContents = "BYTES COLLECTED FROM CLIENT 2"
  else:
    f = open(f"./ServerFiles/{fileName}", "r")
    data = f.read()
    fileObj.fileContents = data.encode(FORMAT)
    
    f.close()
    # the server has the file

  return (existsOnServer, fileObj.fileContents)

def CreateFile(fileName):
  if os.path.exists(f"./ServerFiles/{fileName}"):
    print(f"File already exist")
  else:
    print()
    # create the file
  
  
def Main():
  # bind the socket to the correct host and port
  # prints an error if the socket cannot be bound
  try:
    s.bind((HOST, PORT))

  except s.error() as socketError:
    print(str(socketError))

  while True:
    s.listen(5)
    print("Socket is listening")

    # this does work
    conn, addr = s.accept()
    clients.append((conn, addr))
    global numClients
    numClients += 1
    
    client1Addr = clients[0][1][0]
    client1Port = clients[0][1][1]
    client2Addr = None
    client2Port = None
    
    if numClients == 2:
      client2Addr = clients[1][1][0]
      client2Port = clients[1][1][1]

    
    # print(f"Connected to {addr[0]}:{addr[1]}")
    print(f"CLIENT1 = Address: {client1Addr}\n Port: {client1Port}\n")
    print(f"CLIENT2 = Address: {client2Addr}\n Port: {client2Port}\n")

    thread.start_new_thread(HandleClient, (clients[0][0], ))
    global numThreads
    numThreads += 1

  # server should never reach this line of code unless we break from the above loop
  s.close()


if __name__ == '__main__':
  Main()
