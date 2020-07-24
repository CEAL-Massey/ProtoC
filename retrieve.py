# Secondary side  of database operation to retrieve data regularly 
# and place in CSV for graph to render from 

import socket
import database
import csv

recent = 0

while True:
	latest = database.retrieve_entry() #Take latest entry from MySQL Database
	if recent != latest:
		with open('C:/Users/Sam Holm/Desktop/Quick Access Stuff Mk 4/Massey 2020/Capstone/WebsiteDjango/mysite/CEAL/templates/CEAL/readings.csv', 'a') as csv_file:
			csv_writer = csv.writer(csv_file, delimiter=',')
			csv_writer.writerow(latest) #Drop the latest reading into the txt file
	recent = latest