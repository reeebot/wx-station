#!/usr/bin/python
import sys
import Adafruit_DHT

import subprocess 
import re 
import os 
import time 
import MySQLdb as mdb 
import datetime

import Adafruit_BMP.BMP085 as BMP085

databaseUsername="root"
databasePassword="linklink"
databaseName="wordpress"

sensor = BMP085.BMP085(mode=BMP085.BMP085_ULTRAHIGHRES)

def saveToDatabase(temperature, pressure):

    con=mdb.connect("localhost", databaseUsername, databasePassword, databaseName)
    currentDate=datetime.datetime.now().date()

    now=datetime.datetime.now()
    midnight=datetime.datetime.combine(now.date(),datetime.time())
    minutes=((now-midnight).seconds)/60 #minutes after midnight, use datead$


    with con:
            cur=con.cursor()

            cur.execute("INSERT INTO temperatures (temperature, pressure, dateMeasured, hourMeasured) VALUES (%s, %s, %s,%s)",(temperature, pressure, currentDate, minutes))

    print "Saved readings"
    return "true"


def readInfo():

    temperature = sensor.read_temperature()
    pressure = sensor.read_pressure()

    print "Temperature: %+.1f C" % temperature
    print "Pressure = %.2f hPa" % pressure


    if pressure is not None and temperature is not None:
        return saveToDatabase(temperature, pressure) #success, save the readings
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
