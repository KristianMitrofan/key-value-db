#!/usr/bin/env python3

import socket
import sys
import random

#List of allowed commands
COMMANDS = ["PUT","GET","DELETE","QUERY","TERMINATE"]
MSG_LENGTH = 1024

def handle_command(sockets,command):
    #Check if the first word of the command belongs in the COMMANDS list
    received_data = []
    split_command = command.split(" ",1)
    if split_command[0] in COMMANDS:
        if split_command[0] == "TERMINATE":
            #Closes a specific connection if additional arguments are given
            if len(split_command) >=2 and split_command[1]:
                sock = split_command[1]
                if sock in sockets.keys():
                    sockets[sock].sendall(command.encode("utf-8"))
                    received_data.append(sockets[sock].recv(MSG_LENGTH).decode("utf-8"))
                    sockets[sock].close()
                    #And removes the socket from current connections
                    del sockets[sock]
                else:
                    received_data.append("ERROR: server was not found!")
                
                #If last connection was closed then exit broker too
                if not sockets:
                    print("All connections have been terminated, broker closing too...")
                    exit()
            #Else terminate all the servers and broker
            else:
                for s in sockets.values():
                    s.sendall(command.encode("utf-8"))
                    data = s.recv(MSG_LENGTH)
                    print(data.decode("utf-8"))
                    s.close()

                print("All connections have been terminated, broker closing too...")
                exit()
        elif split_command[0] == "PUT":
            if len(sockets) < kreplication:
                received_data.append("ERROR: there are less than k servers running, so it is not safe to insert an entry!")
            else:
                for s in random.sample(list(sockets.values()),kreplication):
                    s.sendall(command.encode("utf-8"))
                    #Add all the replies to a list
                    received_data.append(s.recv(MSG_LENGTH).decode("utf-8"))
        elif split_command[0] == "DELETE":
            #If even one server is down we cannot delete an entry
            if max_servers > len(sockets):
                received_data.append("ERROR: at least one server is down, entry cannot be deleted!")
            else:
                for s in sockets.values():
                    s.sendall(command.encode("utf-8"))
                    received_data.append(s.recv(MSG_LENGTH).decode("utf-8"))
        else:
            if (max_servers - len(sockets)) >= kreplication:
                received_data.append("ERROR: k or more servers are down so it is not safe to search the entry!")
            else:
                for s in sockets.values():
                    s.sendall(command.encode("utf-8"))
                    received_data.append(s.recv(MSG_LENGTH).decode("utf-8"))

        #Check the replies from all the servers so only one message is shown at the end
        #There should be at least one reply in the received data
        final_msg = received_data[0]
        for reply in received_data:
            #If there is an OK message return that one
            if reply.split(":",1)[0] == "OK":
                final_msg = reply

        print(final_msg)

    else:
        print("ERROR: command is not allowed")


if __name__ == "__main__":
    address_file = "serverFile.txt"
    data_file = "dataToIndex.txt"
    kreplication = 2 

    #kvBroker -s serverFile.txt -i dataToIndex.txt -k 2
    for i, arg in enumerate(sys.argv):
        if arg == "-s":
            address_file = sys.argv[i+1]
        elif arg == "-i":
            data_file = sys.argv[i+1]
        elif arg == "-k":
            kreplication = int(sys.argv[i+1])


    #Read the file with the socket ips and ports
    address_of = open(address_file, "r")
    sockets = {}
    #Connect and store the sockets of all the servers from the serverFile.txt in a dictionary
    for line in address_of:
        host = line.split()[0]
        port = line.split()[1]
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, int(port)))
        #The key of each socket is ""host-port"
        sockets[host + "-" + port] = s

    #Number of servers that the broker initially connects to
    max_servers = len(sockets)

    address_of.close()

    data_of = open(data_file, "r")
    for line in data_of:
        command = "PUT " + line
        handle_command(sockets,command)

    data_of.close()

    #Start accepting commands
    while True:
        command = input("INPUT A COMMAND: ")
        handle_command(sockets,command)
        
