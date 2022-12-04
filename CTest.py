import socket
import threading, _thread as thread

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 54321  # The port used by the server

# def ReadFromServer(server):
#   data = server.recv(1024)

#   print(f"From Server: {data.decode('utf-8')}")


# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#   s.connect((HOST, PORT))

#   thread.start_new_thread(ReadFromServer, (s, ))

#   command, fileName = input("Input Command: ")
  
#   s.send(command.encode('utf-8'))
  

with open("./Client1Files/audio.mp3", "rb") as f1:
  with open("./Client1Files/audio2.mp3", "rb") as f2:
    with open("./Client1Files/MergedFiles", "wb") as merged:
      merged.write(f1.read())
      splitPoint = merged.tell()
      merged.write(f2.read())

    with open("./Client1Files/MergedFiles", "rb") as merged:
      with open("./Client1Files/M1NEW.mp3", "wb") as m1:
        m1.write(merged.read(splitPoint))
      with open("./Client1Files/M2NEW.mp3", "wb") as m2:
        m2.write(merged.read())