#!/usr/bin/env python
#-*- coding: utf-8 -*-

#imports

import time
import sys
import urllib2

sys.path.append('./Adafruit_ADS1x15')

import os
os.chdir("/usr/lib/cgi-bin")

import SDL_Pi_Weather_80422 as SDL_Pi_Weather_80422

# PRINT TO FILE
#sys.stdout = open('wind.php', 'w')


#
# GPIO Numbering Mode GPIO.BCM
#

anenometerPin = 23
rainPin = 24

# constants

SDL_MODE_INTERNAL_AD = 0
SDL_MODE_I2C_ADS1015 = 1

#sample mode means return immediately.  THe wind speed is averaged at sampleTime or when you ask, whichever is longer
SDL_MODE_SAMPLE = 0
#Delay mode means to wait for sampleTime and the average after that time.
SDL_MODE_DELAY = 1

weatherStation = SDL_Pi_Weather_80422.SDL_Pi_Weather_80422(anenometerPin, rainPin, 0,0, SDL_MODE_I2C_ADS1015)

weatherStation.setWindMode(SDL_MODE_SAMPLE, 5.0)
#weatherStation.setWindMode(SDL_MODE_DELAY, 5.0)


totalRain = 0

while True:

        currentWindSpeed = weatherStation.current_wind_speed()/1.852
        currentWindGust = weatherStation.get_wind_gust()/1.852
        direction = weatherStation.current_wind_direction()
        totalRain = totalRain + weatherStation.get_current_rain_total()/25.4
        windspeed = '%0.0f'%(currentWindSpeed)
        windgust = '%0.0f'%(currentWindGust)
        windmph = currentWindSpeed * 1.15
        gustmph = currentWindGust * 1.15
        winddir = str(direction)
        rain = str(totalRain)
        curtime = time.ctime()

        with open('wind.php', 'w') as windfile:
                windfile.write('<p4>' + winddir + '°</p4>' + '</br><p5>' + windspeed + '</p5><p6> kts' + '</p6>')
                windfile.write('<br>to<b> ' + windgust + ' kts</b><p>')
                #windfile.write('<br><br><br>Rain Total: ' + rain + 'in<br><br><br>')
                #windfile.write('<br><br><br><br><br><br>' + curtime + '<br><br><br>')

        with open('winddata.txt', 'w', os.O_NONBLOCK) as datafile:
                datafile.write(winddir + "\n" + '%0.0f'%(windmph) + "\n" + '%0.0f'%(gustmph) + "\n")


        time.sleep(10.0)
