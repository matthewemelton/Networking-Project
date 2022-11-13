import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65412  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  s.connect((HOST, PORT))

  data = s.recv(1024)
  ID = data.decode('utf-8')
  print(f"My ID is: {ID}")

  # send command to server
  sendData = input("Command for server: ")
  s.send(sendData.encode('utf-8'))

  # wait for response
  data = s.recv(1024)
  print(f"Data from server: {data.decode('utf-8')}")