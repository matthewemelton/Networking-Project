# this is the server for the Fall 2022 CS 371 Project

import socket, threading, _thread as thread, os
from FileClass import File

print_lock = threading.Lock()

FORMAT = "utf-8"

numClients = 0
numThreads = 0
clients = []
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if not os.path.exists("./ServerFiles"):
    os.mkdir("./ServerFiles")


HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 55321  # Port to listen on (non-privileged ports are > 1023)
fileStorage = {}


def Upload(fileName, connection):
    # We may need try/except here if client doesn't have the file

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
    existsOnServer, fileObj = GetFile(fileName)
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

    # If the file exists in fileStorage, then it is already in ./ServerFiles
    if fileName in fileStorage:
        fileObj = fileStorage[fileName]

        with open(f"./ServerFiles/{fileName}", "r") as f:
            data = f.read()
            fileObj.initBytesGivenContent(data)

    # If the file does not exist in fileStorage, then we need client 2 to upload the file to the server temporarily for client 1 to receive it
    else:
        existsOnServer = False

        client2Connection = None  # Change this to be the client 2 connection object

        # Using upload here downloads the file from client 2 onto the server. The file will need to be deleted from the server after client 1 receives it
        Upload(fileName, client2Connection)

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

        thread.start_new_thread(HandleClient, (clients[0][0],))
        global numThreads
        numThreads += 1

    # server should never reach this line of code unless we break from the above loop
    s.close()


if __name__ == "__main__":
    Main()
