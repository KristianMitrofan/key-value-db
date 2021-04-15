#!/usr/bin/env python3
import sys
import json
import socket
import kvTrie

MSG_LENGTH = 1024

def error_message(conn,msg):
    encoded_msg = ("ERROR: " + msg).encode("utf-8")
    conn.sendall(encoded_msg)

def success_message(conn,msg):
    encoded_msg = ("OK: " + msg).encode("utf-8")
    conn.sendall(encoded_msg)

def not_found_message(conn,msg):
    encoded_msg = ("NOT FOUND: " + msg).encode("utf-8")
    conn.sendall(encoded_msg)

def execute_command(sock,conn,trie,command):
    split_command = command.split(" ",1)
    
    if(split_command[0] == "TERMINATE"):
        #host, port = sock.getpeername()
        ## getting the IP address using socket.gethostbyname() method
        host = sock.getsockname()[0]
        port = sock.getsockname()[1]
        del(trie)
        success_message(conn,"Server with ip: " + host + " and port: " + str(port) + " has terminated!")
        sock.close()
    else:
        if len(split_command) >=2 and split_command[1]:
            command = split_command[0]
            data = split_command[1]
            #PUT "person1" : { "name" : "John" ; "age" : 22 }
            if command == "PUT":
                #Split data into key and value
                data = data.split(":",1)
                if len(data) >=2 and data[1]:
                    key = data[0].replace("\"","").strip()
                    value = data[1].replace(";",",").strip()
                    try:
                        dict_value = json.loads(value)
                        trie.insert(key,dict_value)
                        success_message(conn,value + " was inserted!")
                    except:
                        error_message(conn,"data is in the wrong format!")
            #GET person1
            elif command == "GET":
                key = data.replace("\"","").replace("."," ").strip()
                value = trie.search(key)
                if value is not None:
                    success_message(conn,key + " : " + value)
                else:
                    not_found_message(conn,data + " could not be found!")
            #DELETE person1
            elif command == "DELETE":
                key = data.replace("\"","").strip()
                if trie.delete(key):
                    success_message(conn,key + " was deleted!")
                else:
                    not_found_message(conn,key + " could not be found!")
            #QUERY person1.age
            elif command == "QUERY":
                key = data.replace("\"","").strip()
                value = trie.search(key)
                if value is not None:
                    success_message(conn,key + " : " + value)
                else:
                    not_found_message(conn,data + " could not be found!")

        else:
            error_message(conn,"no data sent along with command!")

if __name__ == "__main__":
    #Default values
    host = '127.0.0.1' 
    port = 65432
    #kvServer -a ip_address -p port
    for i, arg in enumerate(sys.argv):
        if arg == "-a":
            ip_address = sys.argv[i+1]
        elif arg == "-p":
            port = int(sys.argv[i+1])

    trie = kvTrie.KV_Trie()
    #Create and bind the socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    #Listen for a connection from the kvBroker
    s.listen()
    conn, addr = s.accept()
    with conn:
        print("Connected by kvBroker " + host + " using port " + str(port))
        while True:
            data = conn.recv(MSG_LENGTH)
            if not data:
                break
            else:
                command = data.decode("utf-8")
                execute_command(s,conn,trie,command)

    del(trie)    
    s.close()