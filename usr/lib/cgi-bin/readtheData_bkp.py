#!/usr/bin/env python
import os
os.chdir("/usr/lib/cgi-bin")

import time
import sys
import urllib2
import Adafruit_DHT
import Adafruit_BMP.BMP085 as BMP085
sys.path.append('./Adafruit_ADS1x15')
import SDL_Pi_Weather_80422 as SDL_Pi_Weather_80422
from tentacle_pi.AM2315 import AM2315
am = AM2315(0x5c,"/dev/i2c-1")
import SI1145.SI1145 as SI1145


# PRINT TO FILE
#sys.stdout = open('temperature.php', 'w')

# BMP180
sensorbmp = BMP085.BMP085(mode=BMP085.BMP085_ULTRAHIGHRES)
# AM2315
temperature, humidity, crc_check = am.sense()
Fahrenheit = 9.0/5.0 * temperature + 32
# SI1145 # not working?
# sensorsi = SI1145.SI1145()


# CONVERSIONS ETC
inttemperature = sensorbmp.read_temperature() #internal temperature
pressure = sensorbmp.read_pressure() #station pressure
mb = sensorbmp.read_sealevel_pressure() * 0.01 #sea level pressure mb
inhg = sensorbmp.read_sealevel_pressure() * 0.000295299830714 #altimeter setting inHg
ft = sensorbmp.read_altitude() * 3.280839895 #pressure altitude ft
density = ft + (120 * (temperature - 3.16233)) #density altitude ft
dewpointC = temperature - ((100 - humidity)/5) #dewpoint C  Td = T - ((100 - RH)/5.)
dewpoint = 9.0/5.0 * dewpointC + 32 #dewpoint F
curtime = time.ctime() #current time
#UV = sensorsi.readUV() #uv sensor
#uvIndex = UV / 100.0 #uv sensor

# DEW POINT
realDPC = ((humidity/100)**0.125)*(112+0.9*temperature)+0.1*temperature-112
realDP = 9.0/5.0 * realDPC + 32

# PRINT
#print "<br><b>hilltopWx</b><br><i>5975'</i><br>"
##print "<br><br><h2>%0.1f""&deg;F</h2>" % (Fahrenheit) #/ %0.1f""&deg;C  (temperature) celcius
##print "<b>%0.1f&deg;F Dewpoint<br>%0.1f%% Humidity<br><br><br><br><br></b>" % (realDP, humidity)
#print "<i>%+.1f&deg;C (internal temp)</i><br><br>" % inttemperature

#print "Station Pressure: %.2f Pa<br>" % pressure
##print "{0:0.2f} inHg<br>".format(inhg)
##print "{0:0.0f}' Density Altitude<br><br>".format(density)
#print "Pressure Altitude: {0:0.0f}ft<br>".format(ft)
#print '%0.1f UV Index<br><br><br><br>' % (uvIndex)

####
with open('temperature.php', 'w') as temperaturefile:
	temperaturefile.write('<br><br><h2>%0.0f&deg;F</h2>' % (Fahrenheit))
	temperaturefile.write('<b>%0.0f%% RH<b><br><br>' % (humidity)) #%0.1f&deg;F Dewpoint (realDP)
	temperaturefile.write('<h3>{0:0.2f} inHg</h3><br><br><br>'.format(inhg))

with open('tempdata.txt', 'w') as datafile:  #automatically closes file when done
    datafile.write('{0:0.1f}'.format(Fahrenheit) + "\n")
    datafile.write('{0:0.1f}'.format(realDP) + "\n")
    datafile.write('{0:0.0f}'.format(humidity) + "\n")
    datafile.write('{0:0.2f}'.format(inhg) + "\n")


#SEND TO WU
#urlWU = "http://rtupdate.wunderground.com/weatherstation/updateweatherstation.php?ID=KCOFORTC162&PASSWORD=imporlink&dateutc=now&tempf={0}&baromin={1}&dewptf={2}&humidity={3}&action=updateraw&realtime=1&rtfreq=2.5".format(Fahrenheit, inhg, realDP, humidity)
#urllib2.urlopen(urlWU).read() #send data to Weather Underground



#print "Sun Data"
#print "Moon Data"

