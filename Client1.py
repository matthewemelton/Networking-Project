# this is client 1 for the Fall 2022 CS 371 Project

import socket, os, time, datetime, sys
import threading, _thread as thread
# import pyaudio, wave, pickle, struct

# clientDirectory = Directory()

# HOST = "127.0.0.1"  # The server's hostname or IP address
# PORT = 54321  # The port used by the server
FORMAT = "utf-8"  # The encoding format used for the file
downloadDict = {}
waitingOnServer = False
HOST, PORT = "127.0.0.1", 8001
CHUNK = 2056
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if not os.path.exists("./Client1Files"):
  os.mkdir("./Client1Files")


def ListenForServer():
  time.sleep(0.5)
  s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s2.connect((HOST, PORT + 1))
  global waitingOnServer
  while True:
      data = s2.recv(1024)
      data = data.decode(FORMAT)
      print(f"[{data}]")
      splitData = data.split()
  
      if splitData[0] == "CHECK":
        filename = splitData[1]
  
        Check(filename, s2)
        time.sleep(1)



def Check(fileName, s2):
  global HOST, PORT
  

  if os.path.isfile(f"./Client1Files/{fileName}"):
    # Send the info to the server in the format: COMMAND fileName
    # Spaces are being used as the delimeters
    s2.send("YES".encode(FORMAT))
    time.sleep(
      0.01
    )  # This sleep ensures that they get sent as seperate transmissions

    with open(f"./Client1Files/{fileName}", "rb") as f:
      frame = f.read(CHUNK)
      while len(frame) == CHUNK:
        s2.send(frame)
        frame = f.read(CHUNK)
      s2.send(frame)
    
    # get ACK from server
    result = s2.recv(CHUNK)
    if result.decode(FORMAT) != "ACK":
      print("ERROR in check upload..\n")
      
      
  else:
    s2.send("NO".encode(FORMAT))


def UploadTextFile(fileName):
  global s
  filePath = f"./Client1Files/{fileName}"
  t0 = time.time()  # Start timer
  # Check if the user provided a valid file name

  if os.path.isfile(filePath):

    # Open the file
    with open(filePath, "r") as f:
      data = f.read()  # Read the data from the file
      # Send the info to the server in the format: COMMAND fileName
      # Spaces are being used as the delimeters
      s.send(b"UPLOAD " + fileName.encode(FORMAT))
      time.sleep(
        0.01
      )  # This sleep ensures that they get sent as seperate transmissions
      # Send the data
      s.send(data.encode(FORMAT))
  else:
    print("ERROR: file does not exist\n")
      
  t1 = time.time()  # End timer
  print(f"UPLOAD ran for: {t1-t0} \n")

def UploadMediaFile(fileName):
  global s
  filePath = f"./Client1Files/{fileName}"
  t0 = time.time()  # Start timer

  if os.path.isfile(filePath):
    with open(filePath, "rb") as f:
      s.send(b"UPLOAD " + fileName.encode(FORMAT))
      time.sleep(
        0.01
      )  # This sleep ensures that they get sent as seperate transmissions

      fileSize = round(os.path.getsize(filePath) / 1000000, 2)
      fileSize = str(fileSize)
      s.send(fileSize.encode(FORMAT))
      time.sleep(
        0.01
      )  # This sleep ensures that they get sent as seperate transmissions

      frame = f.read(CHUNK)
      while len(frame) == CHUNK:
        s.send(frame)
        frame = f.read(CHUNK)
      
      # still need to send the last frame
      s.send(frame)
      print("File Sent\n")

      # print("Sending EOF byte\n")
      # temp = b"\n"
      # s.send(temp)

      print("waiting for ACK from server\n")
      byte = s.recv(10)
      while byte != b"ACK":
        byte = s.recv(10)
      print("ACK recieved\n")
  else:
    print("ERROR: file does not exist\n")
      
  t1 = time.time()  # End timer
  print(f"UPLOAD ran for: {t1-t0} \n")
  


def Connect(HOST, PORT):
  global s
  t0 = time.time()  # Start timer

  s.connect((HOST, PORT))

  t1 = time.time()  # End timer
  print(f"CONNECT ran for: {t1-t0}\n")  # Print how long the task took


def Download(files):
  global s
  t0 = time.time()  # Start timer
  s.send("DOWNLOAD ".encode(FORMAT) + fileName.encode(FORMAT))

  # print("waiting for data\n")
  # data = s.recv(1024)  # Receive data from the server
  # data = data.decode(FORMAT)
  # print(f"received data {data}\n")

  # if data == "DNE":
  #   print("File not found on server or client 2")
  #   t1 = time.time()
  #   print(f"DOWNLOAD ran for: {t1-t0} \n")

  #   return

  # print("File recieved from server")

  temp = s.recv(CHUNK).decode().split()
  result = temp[0]


  if result == "YES":
    fileSize = temp[1]
    # recieve and write the file
    print("File is downloading...")
    with open(f"./Client1Files/{fileName}", "wb") as f:
      frame = s.recv(CHUNK)
      while len(frame) == CHUNK:
        f.write(frame)
        bytesReceived = round(os.path.getsize("./ServerFiles/" + fileName), 2) / 1000000
        print(f"received {bytesReceived} / {fileSize} MB                      ")
        sys.stdout.write("\033[F")
        frame = s.recv(CHUNK)
      f.write(frame) # dont forget about the last frame

    s.send("ACK".encode(FORMAT))  # Send ACK to server
    t1 = time.time()  # End timer
    print(f"DOWNLOAD ran for: {t1-t0} \n")

  else:
    print("File does not exist on server or other client...\n")


def Delete(fileName):
  t0 = time.time()  # Start timer
  # if os.path.isfile(fileName):
  #   os.remove(fileName)
  # else:
  #   print("ERROR: file does not exist\n")

  # Send the DELETE command to the server with the file name
  s.send(b"DELETE " + fileName.encode(FORMAT))

  t1 = time.time()  # End timer
  print(f"DELETE ran for: {t1-t0}\n")


def Dir():
  t0 = time.time()  # Start timer

  # Send the DIR command to the server
  s.send(b"DIR")

  data = s.recv(1024)  # Receive data from the server
  data = data.decode(FORMAT)

  print(data)  # Print data to user on client machine

  t1 = time.time()  # End timer
  print(f"DIR ran for: {t1-t0} \n")

def Scenario2_1(file1, file2):
  t0 = time.time() # start the timer for scenario 2_1
  request = f"2_1 {file1} {file2}"
  s.send(request.encode(FORMAT))

  # recieve the first file
  with open(f"./Client1Files/{file1}", "wb") as f:
    frame = s.recv(CHUNK)
    while len(frame) == CHUNK:
      f.write(frame)
      frame = s.recv(CHUNK)
    f.write(frame)

  # send ACK to server
  ACK = "ACK"
  s.send(ACK.encode(FORMAT))

  # recieve the second file
  with open(f"./Client1Files/{file2}", "wb") as f:
    frame = s.recv(CHUNK)
    while len(frame) == CHUNK:
      f.write(frame)
      frame = s.recv(CHUNK)
    f.write(frame)
  
  # send ACK to server
  ACK = "ACK"
  s.send(ACK.encode(FORMAT))
  
  t1 = time.time()
  totalTime = t1-t0

  # delete the files for the next test
  os.remove(f"./Client1Files/{file1}")
  os.remove(f"./Client1Files/{file2}")

  return totalTime

def Scenario2_2(file1, file2):
  data = None

def Scenario2_3(file1, file2):
  t0 = time.time() # start the timer for scenario 2_1
  request = f"2_3 {file1} {file2}"
  s.send(request.encode(FORMAT))

  # recieve the first file
  with open(f"./Client1Files/{file1}", "wb") as f:
    frame = s.recv(CHUNK)
    while len(frame) == CHUNK:
      f.write(frame)
      frame = s.recv(CHUNK)
    f.write(frame)
  
  # recieve the second file
  with open(f"./Client1Files/{file2}", "wb") as f:
    frame = s.recv(CHUNK)
    while len(frame) == CHUNK:
      f.write(frame)
      frame = s.recv(CHUNK)
    f.write(frame)
  
  t1 = time.time()
  return t1-t0
  


def RunTest(file1, file2):
  # run scenario 2-1
  print("Running test for Scenario 2...\n")

  result = Scenario2_1(file1, file2)
  print(f"Strategy 2-1 took {round(result, 2)} seconds\n")

  result = Scenario2_3(file1, file2)
  print(f"Strategy 2-3 took {round(result, 2)} seconds\n")


def Main():
  global waitingOnServer

  while True:
    if not waitingOnServer:
      # Get the commmand and filename (if applicable) from the user
      userInput = input("Enter your command: ")
      command = None
      

      # separate the user input based on the delimeter (spaces)
      splitInput = userInput.split()

      # the first component of the user input should always be the command
      command = splitInput[0]

      if len(splitInput) > 4:
        print("ERROR: too many files requested")
      else:
        numFiles = len(splitInput) - 1

      
      files = splitInput[1:]
      # Separate the command and filename into separate variables
      # if userInput != "DIR":
      #  command, fileName = userInput.split()

      # else:
      #  Dir()

      # upload a file if that is what the user has commanded
      if command == "UPLOAD":
        for file in files:
          # if file.endswith(".txt"):
          #   UploadTextFile(file)
          # else:
          UploadMediaFile(file)
          time.sleep(2.5)

      # download a file from the server if that is what the user commanded
      elif command == "DOWNLOAD":
        Download(files)

      # delete the file specified by the user
      elif command == "DELETE":
        fileName = splitInput[1]
        Delete(fileName)

      elif command == "CHECK":
        fileName = splitInput[1]

      # connect to the specified host and port
      elif command == "CONNECT":
        global HOST, PORT
        HOST, PORT = splitInput[1:]
        PORT = int(PORT)
        Connect(HOST, PORT)
        thread.start_new_thread(ListenForServer, ())

      # print the contents of the server directory
      elif command == "DIR":
        Dir()

      elif command == "RUN_TEST":
        RunTest(splitInput[1], splitInput[2])

      else:
        print("ERROR: Invalid command")


if __name__ == "__main__":
  Main()
