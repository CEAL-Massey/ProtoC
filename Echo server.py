#!/usr/bin/env python3

import socket
import proto_struct_pb2
import database
import csv
import pandas as pd

HOST = '192.168.1.3'  
PORT = 8887     # Port to listen on (non-privileged ports are > 1023)

struct = proto_struct_pb2.sens_dat()

load = [0,0,0]
flag = 0
ovf = 0
prev_array = [0,0]

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            data = conn.recv(1024)
            struct.ParseFromString(data) #De-serialize string into struct
            #database.insert_entry(struct) #Load entry into MySQL database
            readings = pd.read_csv('C:/Users/Sam Holm/Desktop/Quick Access Stuff Mk 4/Massey 2020/Capstone/WebsiteDjango/mysite/CEAL/templates/CEAL/readings.csv')
            if (readings.shape[0] >= 50):
                readings.drop([0], inplace = True) #Keep the csv at approximately 20 entries
            as_array = [struct.timestamp, struct.data]
            if ((prev_array != as_array) and (flag == 1) and (prev_array[1] != ovf)):
                load = [prev_array[0], prev_array[1], as_array[1]]
                readings = readings.append(pd.Series(load, index=readings.columns), ignore_index = True)
                ovf = as_array[1]
            prev_array = as_array
            flag = 1
            readings.to_csv(r'C:/Users/Sam Holm/Desktop/Quick Access Stuff Mk 4/Massey 2020/Capstone/WebsiteDjango/mysite/CEAL/templates/CEAL/readings.csv', index = False)
            conn.sendall(data)
            s.close()