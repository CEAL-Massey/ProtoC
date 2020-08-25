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
                readings.drop([0], inplace = True)
            as_array = [struct.timestamp, struct.data]
            readings = readings.append(pd.Series(as_array, index=readings.columns), ignore_index = True)
            readings.to_csv(r'C:/Users/Sam Holm/Desktop/Quick Access Stuff Mk 4/Massey 2020/Capstone/WebsiteDjango/mysite/CEAL/templates/CEAL/readings.csv', index = False)
            
            # with open('C:/Users/Sam Holm/Desktop/Quick Access Stuff Mk 4/Massey 2020/Capstone/WebsiteDjango/mysite/CEAL/templates/CEAL/readings.csv', 'a', newline = '') as csv_file:
            #     #check contents - is there 20 entries? if so, remove oldest and then add
            #     #add new entry
            #     csv_reader = csv.reader(csv_file, delimiter = ',')
            #     data = list(csv_reader)
            #     count = len(data)
            #     if count >= 20:
            #         data.remove(row[0])
            #     end
            #     csv_writer = csv.writer(csv_file, delimiter = ',')
            #     as_array = [struct.timestamp, struct.data,',']
            #     print(as_array)
            #     csv_writer.writerow(as_array) #Drop the latest reading into the txt file        
            # #if not data:
            # #    break
            conn.sendall(data)
            s.close()