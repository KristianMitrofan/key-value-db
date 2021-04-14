#!/usr/bin/env python3

import socket

#List of allowed commands
COMMANDS = ["PUT","GET","DELETE","QUERY","TERMINATE"]

def handle_command(sockets,command):
    #Check if the first word of the command belongs in the COMMANDS list
    if command.split(" ",1)[0] in COMMANDS:
        #Closes all connections with the servers receiving a message from each of them and exits
        if command == "TERMINATE":
            for s in sockets:
                s.sendall(command.encode("utf-8"))
                data = s.recv(1024)
                print(data.decode("utf-8"))
                s.close()

            exit()
        else:
            for s in sockets:
                s.sendall(command.encode("utf-8"))
                data = s.recv(1024)
                print(data.decode("utf-8"))

    else:
        print("ERROR: command is not allowed")


if __name__ == "__main__":
    address_file = "serverFile.txt"
    data_file = "dataToIndex.txt"

    #Read the file with the socket ips and ports
    address_of = open(address_file, "r")
    sockets = []
    #Connect and store the sockets of all the servers from the serverFile.txt in a list
    for line in address_of:
        host = line.split()[0]
        port = line.split()[1]
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, int(port)))
        sockets.append(s)

    address_of.close()

    data_of = open(data_file, "r")
    for line in data_of:
        command = "PUT " + line
        handle_command(sockets,command)
        

    data_of.close()


    #Start accepting commands
    while True:
        command = input("Input an element: ")
        handle_command(sockets,command)
        
