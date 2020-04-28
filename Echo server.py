#!/usr/bin/env python3

import socket
import proto_struct_pb2


HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

struct = proto_struct_pb2.sens_dat()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            struct.ParseFromString(data)
            print(struct)
            if not data:
                break
            conn.sendall(data)
 
