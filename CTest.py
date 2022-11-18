import socket
import threading, _thread as thread

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 54321  # The port used by the server

def ReadFromServer(server):
  data = server.recv(1024)

  print(f"From Server: {data.decode('utf-8')}")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  s.connect((HOST, PORT))

  thread.start_new_thread(ReadFromServer, (s, ))

  command, fileName = input("Input Command: ")
  
  s.send(command.encode('utf-8'))
  
  