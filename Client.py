# this is client 1 for the Fall 2022 CS 371 Project

import socket, os, time, datetime

# clientDirectory = Directory()

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 54321  # The port used by the server
FORMAT = 'utf-8' # The encoding format used for the file
downloadDict = {}
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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

def Connect():
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
  if os.path.isfile(fileName):
    os.remove(fileName)
  else:
    print("ERROR: file does not exist\n")
      
  t1 = time.time() # End timer
  print(f"DELETE ran for: {t1-t0}\n")

def Dir(fileName):
  t0 = time.time()
  # for os.listdir(path):
  
  if os.path.isfile(fileName):
    print("File Name: " + fileName + "\n")
    print("File Size: " + os.path.getsize(fileName) + "\n")
    #TODO: figure out how to track upload date and time
    #TODO: figure out how to track number of downloads
  else:
    print("ERROR: file does not exist \n")
  t1 = time.time()
  print(f"DIR ran for: {t1-t0} \n")


  
def Main():
  while True: 
    # Get the commmand and filename (if applicable) from the user
    userInput = input("Enter your command: ")
    command = None
    print(f"\n\n\n{userInput}\n\n\n")
    
    # Separate the command and filename into separate variables
    if userInput != "CONNECT":
      command, fileName = userInput.split()

    else:
      Connect()
      
    # upload a file if that is what the user has commanded
    if command == "UPLOAD":
      Upload(fileName)
      
    # download a file from the server if that is what the user commanded
    elif command == "DOWNLOAD":
      Download(fileName)
      
    # delete the file specified by the user
    elif command == "DELETE":
      Delete(fileName)
   
    # return the content of the folder
    elif command == "DIR":
      Dir(fileName)
      
if __name__ == '__main__':
  Main()
