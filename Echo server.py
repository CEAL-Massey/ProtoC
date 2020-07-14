#!/usr/bin/env python3

import socket
import proto_struct_pb2
import database

HOST = '192.168.20.9'  
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

struct = proto_struct_pb2.sens_dat()

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            data = conn.recv(1024)
            struct.ParseFromString(data) #De-serialize string into struct
            print(struct)
            database.insert_entry(struct) #Load entry into MySQL database
            if not data:
                break
            conn.sendall(data)
 
