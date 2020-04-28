#!/usr/bin/env python3

import socket
import proto_struct_pb2
import datetime


HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server


time = datetime.datetime.today()
time = time.strftime('%Y%m%d%H%M%S')


sensor = proto_struct_pb2.sens_dat()
sensor.type = "temp"
sensor.unit = "celcius"
sensor.timestamp = time
sensor.data = 24.5

to_send = sensor.SerializeToString()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    s.sendall(to_send)
    data = s.recv(1024)

print('Received', repr(data))