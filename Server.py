# this is the server for the Fall 2022 CS 371 Project

import socket, threading, _thread as thread, os
from FileClass import File

print_lock = threading.Lock()

FORMAT = "utf-8"

numClients = 0
numThreads = 0
clients = {}
client1, client2 = 0
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if not os.path.exists("./ServerFiles"):
    os.mkdir("./ServerFiles")


HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 54321  # Port to listen on (non-privileged ports are > 1023)
fileStorage = {}


def Upload(fileName, connection):

    fileBytes = connection.recv(1024)

    fileStorage[fileName] = File(fileName)
    fileObj = fileStorage[fileName]

    fileObj.initContentGivenBytes(fileBytes)
    fileObj.addFileToServer()

    print(
        f"""
  {fileObj.name}
  {fileObj.path}
  {fileObj.fileSize}
  {fileObj.downloads}
  {fileObj.fileContents}
  """
    )


def Download(fileName, connection):
    existsOnServer, fileObj = GetFile(fileName, connection)
    fileObj = fileStorage[fileName]

    connection.sendall(fileObj.fileBytes)

    fileObj.downloads += 1

    print(
        f"""
  {fileObj.name}
  {fileObj.path}
  {fileObj.fileSize}
  {fileObj.downloads}
  {fileObj.fileContents}
  """
    )

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
  global numThreads, numClients, clients
  clientID = numClients
  clients[clientID] = connection

  while True:
    # wait for the client to send a command
    data = connection.recv(1024)
    data = data.decode(FORMAT)
    print(f"\n\n{data}\n\n")
    
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
  

def GetFile(fileName, connection):
    existsOnServer = True

    # If the file exists in fileStorage, then it is already in ./ServerFiles
    if fileName in fileStorage:
        fileObj = fileStorage[fileName]

        with open(f"./ServerFiles/{fileName}", "r") as f:
            data = f.read()
            fileObj.initBytesGivenContent(data)

    # If the file does not exist in fileStorage, then we need client 2 to upload the file to the server temporarily for client 1 to receive it
    else:
        existsOnServer = False

        
        if(connection == clients[1]):  # Change this to be the client 2 connection object
            otherClient = clients[2]
        else:
            otherClient = clients[1]
        # Using upload here downloads the file from client 2 onto the server. The file will need to be deleted from the server after client 1 receives it
        Upload(fileName, otherClient)

        # fileName will always exist in fileStorage as long as client 2 has the file, because the Upload adds it
        fileObj = fileStorage[fileName]

    return (existsOnServer, fileObj)


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

        thread.start_new_thread(HandleClient, (conn, ))
        global numThreads
        numThreads += 1
        if(numThreads == 2):
            global clients, client1, client2
            client1 = clients[1]
            client2 = clients[2]

    # server should never reach this line of code unless we break from the above loop
    s.close()


if __name__ == "__main__":
    Main()
