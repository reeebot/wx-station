#!/usr/bin/python
import sys
import Adafruit_DHT

import subprocess 
import re 
import os 
import time 
import MySQLdb as mdb 
import datetime

databaseUsername="YOUR USERNAME, USUALLY ROOT"
databasePassword="YOUR PASSWORD!" 
databaseName="WordpressDB" #do not change unless you named the Wordpress database with some other name

sensor=Adafruit_DHT.DHT22 #if not using DHT22, replace with Adafruit_DHT.DHT11 or Adafruit_DHT.AM2302
pinNum=4 #if not using pin number 4, change here

def saveToDatabase(temperature,humidity):

	con=mdb.connect("localhost", databaseUsername, databasePassword, databaseName)
        currentDate=datetime.datetime.now().date()

        now=datetime.datetime.now()
        midnight=datetime.datetime.combine(now.date(),datetime.time())
        minutes=((now-midnight).seconds)/60 #minutes after midnight, use datead$

	
        with con:
                cur=con.cursor()
		
                cur.execute("INSERT INTO temperatures (temperature,humidity, dateMeasured, hourMeasured) VALUES (%s,%s,%s,%s)",(temperature,humidity,currentDate, minutes))

		print "Saved temperature"
		return "true"


def readInfo():

	humidity, temperature = Adafruit_DHT.read_retry(sensor, pinNum)#read_retry - retry getting temperatures for 15 times

	print "Temperature: %.1f C" % temperature
	print "Humidity:    %s %%" % humidity

	if humidity is not None and temperature is not None:
		return saveToDatabase(temperature,humidity) #success, save the readings
	else:
		print 'Failed to get reading. Try again!'
		sys.exit(1)


#check if table is created or if we need to create one
try:
	queryFile=file("createTable.sql","r")

	con=mdb.connect("localhost", databaseUsername,databasePassword,databaseName)
        currentDate=datetime.datetime.now().date()

        with con:
		line=queryFile.readline()
		query=""
		while(line!=""):
			query+=line
			line=queryFile.readline()
		
		cur=con.cursor()
		cur.execute(query)	

        	#now rename the file, because we do not need to recreate the table everytime this script is run
		queryFile.close()
        	os.rename("createTable.sql","createTable.sql.bkp")
	

except IOError:
	pass #table has already been created
	

status=readInfo() #get the readings
