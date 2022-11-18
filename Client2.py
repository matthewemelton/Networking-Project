# this is client 1 for the Fall 2022 CS 371 Project

import socket, os, time, datetime
import threading, _thread as thread

# clientDirectory = Directory()

# HOST = "127.0.0.1"  # The server's hostname or IP address
# PORT = 54321  # The port used by the server
FORMAT = 'utf-8' # The encoding format used for the file
downloadDict = {}
waitingOnServer = False
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def ListenForServer(server):
  global waitingOnServer
  
  while True:
    data = server.recv(1024)
    data = data.decode('utf-8')
    splitData = data.split()

    if splitData[0] == "CHECK":
      filename = "./Client2Files/" + splitData[1]
      Check(filename)
      waitingOnServer = False

    else:
      print(f"From Server: {data}")
      waitingOnServer = False

def Check(fileName):
  if os.path.isfile(fileName):
    with open(fileName, "r") as f:
      data = f.read() # Read the data from the file

      # Send the info to the server in the format: COMMAND fileName
      # Spaces are being used as the delimeters
      s.send(f"YES".encode(FORMAT))
      s.send(data.encode(FORMAT))
  else:
    s.send("NO")

def Upload(fileName):
  global s
  t0 = time.time() # Start timer
      # Check if the user provided a valid file name
  if os.path.isfile(fileName):
    # clientDirectory.fileUploadDateTime[fileName] = datetime.now()
    # clientDirectory.fileDownloads[fileName] = 0
    # clientDirectory.fileSizes[fileName] = os.path.getsize(fileName)

    # Open the file
    with open(fileName, "r") as f:
      data = f.read() # Read the data from the file

      # Send the info to the server in the format: COMMAND fileName
      # Spaces are being used as the delimeters
      s.send(b"UPLOAD " + bytes(fileName.encode(FORMAT)))
      time.sleep(0.01) # This sleep ensures that they get sent as seperate transmissions
      # Send the data
      s.send(data.encode(FORMAT))


  # If not, give an error message
  else:
    print("ERROR: file does not exist\n")
    
  t1 = time.time() # End timer
  print(f"UPLOAD ran for: {t1-t0} \n") 

# Loop indefinitely

def Connect(HOST, PORT):
  global s
  t0 = time.time() # Start timer

  s.connect((HOST, PORT))
  #s.sendall(b"Hello, world")
  #data = s.recv(1024)
  t1 = time.time() # End timer
  print(f"CONNECT ran for: {t1-t0}\n") # Print how long the task took  

def Download(fileName):
  global s
  t0 = time.time() # Start timer
  s.send(b"DOWNLOAD " + bytes(fileName.encode(FORMAT)))

  data = s.recv(1024) # Receive data from the server
  data = data.decode(FORMAT)
  print(f"THIS IS THE DATA {data}")

  with open(fileName, 'w') as f:
    f.write(data) # Write the data received from the server to the new file

  s.send(b"ACK")
  t1 = time.time() # End timer
  print(f"DOWNLOAD ran for: {t1-t0} \n")
  
def Delete(fileName):
  t0 = time.time() # Start timer
  # if os.path.isfile(fileName):
  #   os.remove(fileName)
  # else:
  #   print("ERROR: file does not exist\n")
  s.send(b"DELETE " + bytes(fileName.encode(FORMAT)))
  
  data = s.recv(1024) # Receive data from the server
  data = data.decode(FORMAT)
  print(f"{fileName} has been deleted from the ServerFiles folder on the server.\n")
  
  t1 = time.time() # End timer
  print(f"DELETE ran for: {t1-t0}\n")

def Dir():
  t0 = time.time()
  # for f in os.listdir(path):
  s.send(b"DIR")

  data = s.recv(1024) # Receive data from the server
  data = data.decode(FORMAT)
    
  print(data)

  t1 = time.time()
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
      #if userInput != "DIR":
      #  command, fileName = userInput.split()

      #else:
      #  Dir()
        
      # upload a file if that is what the user has commanded
      if command == "UPLOAD":
        waitingOnServer = True
        fileName = splitInput[1]
        Upload(fileName)
        
      # download a file from the server if that is what the user commanded
      elif command == "DOWNLOAD":
        fileName = splitInput[1]
        Download(fileName)
        
      # delete the file specified by the user
      elif command == "DELETE":
        fileName = splitInput[1]
        Delete(fileName)
        
      elif command == "CHECK":
        fileName =  splitInput[1]
        
      # connect to the specified host and port
      elif command == "CONNECT":
        HOST, PORT = splitInput[1:]
        Connect(HOST, int(PORT))
        thread.start_new_thread(ListenForServer, (s, ))
        
      # print the contents of the server directory
      elif command == "DIR" :
        Dir()

      else:
        print("ERROR: Invalid command")
      
if __name__ == '__main__':
  Main()
