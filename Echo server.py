#!/usr/bin/env python3

import socket
import proto_struct_pb2
import database
import csv
import pandas as pd

HOST = '192.168.20.7'  
PORT = 8886     # Port to listen on (non-privileged ports are > 1023)

struct = proto_struct_pb2.sens_dat()

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
            if (readings.shape[0] >= 20):
                readings.drop([0], inplace = True) #Keep the csv at approximately 20 entries
            as_array = [struct.timestamp, struct.data]
            readings = readings.append(pd.Series(as_array, index=readings.columns), ignore_index = True)
            readings.to_csv(r'C:/Users/Sam Holm/Desktop/Quick Access Stuff Mk 4/Massey 2020/Capstone/WebsiteDjango/mysite/CEAL/templates/CEAL/readings.csv', index = False)
            conn.sendall(data)
            s.close()