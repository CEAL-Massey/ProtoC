import mysql.connector

sensor_base = mysql.connector.connect(
		host = "localhost", # This iwll be implemented on the Raspberry Pi
		user = "root",		# in order to write data to a table consisting of sensor ID,
		passwd = "Plantsrcool123", # reading, and timestamp. Almost identical code would be
		database = "sensor_base"   # used to retrieve data from the server side, but with a
		)						   # different login to avoid RAW type hazards



def insert_entry(structure):
	type = structure.type
	unit = structure.unit
	time_stamp = structure.timestamp
	data = structure.data

	mycursor = sensor_base.cursor()

	com = "INSERT INTO readings (data, metric, type, time_stamp) VALUES (%s, %s, %s, %s)"
	val = (data, unit, type, time_stamp)

	mycursor.execute(com, val)
	sensor_base.commit()
