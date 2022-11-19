# this is the server for the Fall 2022 CS 371 Project

import socket, threading, _thread as thread, os, time
from FileClass import File

print_lock = threading.Lock()

FORMAT = "utf-8"

numClients = 0
numThreads = 0
clients = {}
client1 = 0
client2 = 0
checking = False
checkData = 0
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if not os.path.exists("./ServerFiles"):
    os.mkdir("./ServerFiles")

# HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
HOST = "127.0.0.1"
PORT = 8000  # Port to listen on (non-privileged ports are > 1023)
fileStorage = {}


def OnStart():
    serverFiles = os.listdir("./ServerFiles")
    print(serverFiles)

    for fileName in serverFiles:
        fileStorage[fileName] = File(fileName)
        fileObj = fileStorage[fileName]

        fileObj.loadFileSize()


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


def Download(fileName, connection, checkConnection):
    existsOnServer, existsOnClient, fileObj = GetFile(
        fileName, connection, checkConnection
    )

    # if not existsOnServer and existsOnClient:
    #   with open(f"./ServerFiles/{fileName}", "r") as f:
    #     data = f.read()
    #     fileObj.initBytesGivenContent(data)

    if not existsOnServer and not existsOnClient:
        connection.send("DNE".encode(FORMAT))
        return

    print("Sending requested file to client")

    connection.send(fileObj.fileBytes)

    fileObj.downloads += 1

    print(
        f"""
  File: {fileObj.name}
  File Path: {fileObj.path}
  Size: {fileObj.fileSize}
  Downloads: {fileObj.downloads}
  Content: {fileObj.fileContents}
  """
    )

    # listen for acknowledgement from client
    print("waiting on ACK from Client")
    ackData = connection.recv(1024)
    # decode acknowledgement
    ackData = ackData.decode(FORMAT)
    # confirm acknowledgement is in proper format
    if ackData == "ACK":
        print("ACK RECIEVED")
        # if the file was not originally on the server, delete it
        if not existsOnServer:
            if os.path.isfile(f"./ServerFiles/{fileName}"):
                os.remove(f"./ServerFiles/{fileName}")
                print(f"Removed ./ServerFiles/{fileName}")
            else:
                print("ERROR: file does not exist\n")
    else:
        print("ERROR: no ack from client\n")


def Dir(connection):
    filesInFolder = os.listdir("./ServerFiles")
    print(filesInFolder)

    statistics = ""

    for fileName in filesInFolder:
        fileObj = fileStorage[fileName]
        fileObj.loadStatistics()
        statistics += fileObj.statistics

    connection.send(statistics.encode(FORMAT))


def Delete(fileName, connection):

    if os.path.isfile(f"./ServerFiles/{fileName}"):
        os.remove(f"./ServerFiles/{fileName}")
        del fileStorage[fileName]

    else:
        print("ERROR: file does not exist\n")


def HandleClient(connection, checkConnection):
    # initalize the client and give the client an ID
    global numClients, clients, client1, client2
    print("Client Connected\n")

    if numClients == 2:
        client1 = clients[1]
        client2 = clients[2]

    while True:
        # wait for the client to send a command
        data = connection.recv(1024)
        data = data.decode(FORMAT)
        print(f"\n\n{data}\n\n")
        # Split the message from the client using a space as the delimeter
        clientTransmission = data.split()
        # the first chunk of the message from the client should always be the command keyword
        command = clientTransmission[0]

        # Check which command keyword was send by the client, calling the appropriate helper function
        if command == "UPLOAD":
            fileName = clientTransmission[1]
            Upload(fileName, connection)

        elif command == "DOWNLOAD":
            fileName = clientTransmission[1]
            Download(fileName, connection, checkConnection)

        elif command == "DIR":
            Dir(connection)

        elif command == "DELETE":
            fileName = clientTransmission[1]
            Delete(fileName, connection)

        elif command == "DISCONNECT":
            temp = "GoodBye"
            connection.send(temp.encode(FORMAT))
            connection.close()
            break

        else:
            print("ERROR: Invalid command keyword received\n")


def GetFile(fileName, connection, checkConnection):
    # boolean value indicates whether the file exists on the server
    existsOnServer = True
    existsOnClient = False
    fileObj = None

    # If the file exists in fileStorage, then it is already in ./ServerFiles
    if fileName in fileStorage:
        fileObj = fileStorage[fileName]

        # open the file and put all of the data into fileObj
        with open(f"./ServerFiles/{fileName}", "r") as f:
            data = f.read()
            fileObj.initBytesGivenContent(data)

    # If the file does not exist in fileStorage, then we need client 2 to upload the file to the server temporarily for client 1 to receive it
    else:
        existsOnServer = False

        # send the file to the client
        global numClients, client1, client2
        # check if there are 2 clients connected
        if numClients == 2:
            if (
                checkConnection == client1
            ):  # Change this to be the client 2 connection object
                otherClient = client2
            else:
                otherClient = client1
            # Using upload here downloads the file from client 2 onto the server. The file will need to be deleted from the server after client 1 receives it

            print("FILE NOT FOUND: Checking the other client for the file...\n")

            # print("Post listen, pre accept")
            otherClient.send(f"CHECK {fileName}".encode(FORMAT))

            # c2, addr = s2.accept()

            print(f"Sent CHECK {fileName}")

            result = otherClient.recv(1024).decode(FORMAT)

            if result == "YES":
                existsOnClient = True
                # write the new file
                fileBytes = otherClient.recv(1024)
                fileStorage[fileName] = File(fileName)
                fileObj = fileStorage[fileName]

                fileObj.initContentGivenBytes(fileBytes)

                with open(f"./ServerFiles/{fileName}", "w") as f:
                    f.write(fileObj.fileContents)

    return (existsOnServer, existsOnClient, fileObj)


def Main():
    # bind the socket to the correct host and port
    # prints an error if the socket cannot be bound
    try:
        s.bind((HOST, PORT))
        s2.bind((HOST, PORT + 1))

    except s.error() as socketError:
        print(str(socketError))

    OnStart()

    while True:
        global numThreads, numClients, clients
        s.listen(5)
        print("Socket is listening")

        # this does work
        conn, addr = s.accept()

        s2.listen(5)
        checkConn, addr = s2.accept()

        numClients += 1
        clients[numClients] = checkConn

        thread.start_new_thread(HandleClient, (conn, checkConn))
        numThreads += 1

    # server should never reach this line of code unless we break from the above loop
    s.close()


if __name__ == "__main__":
    Main()
