# this is client 1 for the Fall 2022 CS 371 Project

import socket, os, time, datetime
import threading, _thread as thread

# clientDirectory = Directory()

# HOST = "127.0.0.1"  # The server's hostname or IP address
# PORT = 54321  # The port used by the server
FORMAT = "utf-8"  # The encoding format used for the file
downloadDict = {}
waitingOnServer = False
HOST, PORT = "127.0.0.1", 8000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if not os.path.exists("./ClientFiles"):
  os.mkdir("./ClientFiles")


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
        filename = "./ClientFiles/" + splitData[1]
  
        Check(filename, s2)
        time.sleep(1)



def Check(fileName, s2):
  global HOST, PORT
  

  if os.path.isfile(fileName):
    with open(fileName, "r") as f:
      data = f.read()  # Read the data from the file

      # Send the info to the server in the format: COMMAND fileName
      # Spaces are being used as the delimeters
      s2.send("YES".encode(FORMAT))
      time.sleep(
        0.01
      )  # This sleep ensures that they get sent as seperate transmissions
      s2.send(data.encode(FORMAT))
  else:
    s2.send("NO".encode(FORMAT))


def Upload(fileName):
  global s
  filePath = f"./ClientFiles/{fileName}"
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

  # If not, give an error message
  else:
    print("ERROR: file does not exist\n")

  t1 = time.time()  # End timer
  print(f"UPLOAD ran for: {t1-t0} \n")


# Loop indefinitely


def Connect(HOST, PORT):
  global s
  t0 = time.time()  # Start timer

  s.connect((HOST, PORT))

  t1 = time.time()  # End timer
  print(f"CONNECT ran for: {t1-t0}\n")  # Print how long the task took


def Download(fileName):
  global s
  t0 = time.time()  # Start timer
  s.send("DOWNLOAD ".encode(FORMAT) + fileName.encode(FORMAT))

  print("waiting for data\n")
  data = s.recv(1024)  # Receive data from the server
  data = data.decode(FORMAT)
  print(f"received data {data}\n")

  if data == "DNE":
    print("File not found on server or client 2")
    t1 = time.time()
    print(f"DOWNLOAD ran for: {t1-t0} \n")

    return

  print("File recieved from server")

  with open(f"./ClientFiles/{fileName}", "w") as f:
    f.write(data)  # Write the data received from the server to the new file

  s.send("ACK".encode(FORMAT))  # Send ACK to server
  t1 = time.time()  # End timer
  print(f"DOWNLOAD ran for: {t1-t0} \n")


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


def Main():
  global waitingOnServer

  while True:
    if not waitingOnServer:
      # Get the commmand and filename (if applicable) from the user
      userInput = input("Enter your command: ")
      command = None
      print(f"\n\n\n{userInput}\n\n\n")

      # separate the user input based on the delimeter (spaces)
      splitInput = userInput.split()

      # the first component of the user input should always be the command
      command = splitInput[0]

      # Separate the command and filename into separate variables
      # if userInput != "DIR":
      #  command, fileName = userInput.split()

      # else:
      #  Dir()

      # upload a file if that is what the user has commanded
      if command == "UPLOAD":
        fileName = splitInput[1]
        Upload(fileName)

      # download a file from the server if that is what the user commanded
      elif command == "DOWNLOAD":
        fileName = splitInput[1]
        waitingOnServer = True
        Download(fileName)
        waitingOnServer = False

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

      else:
        print("ERROR: Invalid command")


if __name__ == "__main__":
  Main()
