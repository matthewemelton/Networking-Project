# Networking-Project
Final project source code for CS 371
Team members: Matthew Melton, Dylan Shade, Brennan Graham

This project consists of 3 files, Server.py, Client.py, and FileClass.py. 

To test these programs using a single machine, you can use 127.0.0.1 (localhost) for the host or you can change the address to be your machine's IP to connect another device (change line 24 in Server.py).
Run Client.py on two different machines. Change the files within the ClientFiles directory on each local machine, and you can now use all commands on any of the files found on either of the clients.

## Format of commands:

*CONNECT [IP] **8080**  
UPLOAD [file from client files]  
DOWNLOAD [file from other client or server]  
DELETE [file on server]  
DIR*


## Server.py: 
This program should run on the server machine. It makes a file (./ServerFiles) to hold the files the server receives from the client and this is where any files the server is supposed to start with should be placed. It can use any non-privileged port. The program works as follows:
- Beginning in the Main function, the server binds a socket to the desired host and port
- The program then loops indefinitely, listening for connection requests and from the clients.
- When a valid connection request is received, a new thread is created to handle that client. This thread passes management of the client over to the HandleClient function. The server can handle up to 2 clients at once. The Main fucntion also tracks the address and port information for both clients and prints this information to the console on the server machine.
- Then, in the HandleClient function, the program loops indefinitely while listening for transmissions from its assigned client. When a transmission is received, it is decoded then split into a command and a file name using a space as the delimeter. If the command is "DISCONNECT", then a "GoodBye" message is sent, the connection is closed, and the loop terminates. If any other command is sent, the corresponding function is called to perform the action requested by the client.
- The upload function accepts a file transmitted from the client to the server and stores it on the server, while the download function initiates the transmission of a file from the server to the client, where it should be stored.
- The Download function is invoked whenever a "DOWNLOAD" command is received from the client. The first thing it does is to invoke the GetFile function, which checks if the file exists on the server. If it does, the function returns the file data to the Download function along with a boolean True indicating the file was found on the server rather than the other client. If the file does not exist on the server, it sends a request to the second client (if it exists) with the keyword CHECK and the file name. The client should then send back either the keyword "YES" or "NO", with "YES" indicating the file was found on the second client and "NO" indicating it was not. If the file exists on the second client, it will then send the file and the server will receive it. The file is then added to the files on the server. If the file does not exist on the server or the other client, the keyword "DNE" is sent to the requesting client to indicate the file does not exist. If the file was on client2 rather than the server, a boolean false is returned to the Download function along with the file object to indicate that the file should be deleted from the server once it has been successfully sent to the requesting client. The Download function then sends the file data to the client which requested it. It then increments the counter for the number of times that file has been downloaded by 1 and waits for an ACK from the client. Once the ACK has been received, the file is deleted from the server if it was not originally located there.
- THe Dir function is invoked when the client sends the "DIR" command to the server. It compiles the relevant statistics for every file on the server and sends them back to the client. 

## Client.py:
This program should run on the client machine(s). It can use any non-privileged port. The program works as follows:
- The Main function is called and loops indefinitely
- The program prompts the user to input a command, which may be followed by additional information depending on the command. The command and additional infomration are delimeted by a space (if applicable). The program then checks which command was entered and calls the corresponding function, passing any additional information as arguments. If the user entered an invalid command, an error message is printed to the console on the client machine.
- In the Upload function, the first step is to check if the file specified by the user exists on the client machine. If it does not, an error message is printed to the console on the client machine. Otherwise, the file is opened and read into the variable called "data". The program then sends the command "UPLOAD" followed by a space and the file name specified by the user, which is encoded. THe program then pauses briefly before sending the encoded data from the file to the server. The time is recorded at the beginning and end of the function and the difference between these times is printed to the console on the client machine so the user knows how long this process took.
- In the Connect function, the program calls the connect function from the imported socket package. The time is recorded at the beginning and end of the function and the difference between these times is printed to the console on the client machine so the user knows how long this process took.
- In the Download function, the program sends the command DOWNLOAD and the encoded filename specified by the user in the same transmission, separated by a space. It then receives the data from the server, decodes it, and saves it to a file on the client machine before printing it to the console. The time is recorded at the beginning and end of the function and the difference between these times is printed to the console on the client machine so the user knows how long this process took.
- In the Delete function, the program sends the "DELETE" command to the server along with the name of the file which the user wants to delete from the server. It then waits for an acknowledgement from the server before printing confirmation to the user. The time is recorded at the beginning and end of the function and the difference between these times is printed to the console on the client machine so the user knows how long this process took.
- In the Dir function, the program sends the "DIR" command to the server, receives the statistics about the files from the server, then prints them to the user on the client machine. The time is recorded at the beginning and end of the function and the difference between these times is printed to the console on the client machine so the user knows how long this process took.

## FileClass.py
This program includes the declaration of our File class. This File class is used to store relevant statistics for each file into a single object. We also use the File class as a middle man to convert bytes to strings and vice versa.