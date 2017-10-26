#!/usr/bin/env python
#
# SDL_Pi_Weather_80422 Example Test File 
# Version 1.0 February 12, 2015
#
# SwitchDoc Labs
# www.switchdoc.com
#
#


#imports

import time
import sys

sys.path.append('./Adafruit_ADS1x15')


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
        currentWindGust = weatherStation.get_wind_gust()/1.6
        direction = weatherStation.current_wind_direction()
        totalRain = totalRain + weatherStation.get_current_rain_total()/25.4
        windspeed = '%0.0f'%(currentWindSpeed)
        windgust = str(currentWindGust)
        winddir = str(direction)
        rain = str(totalRain)

        with open('wind.php', 'w') as windfile:  #automatically closes file when done
        	windfile.write(winddir + ' Degrees' + ' at ')
        	windfile.write(windspeed + ' Knots' + '\n')
        	#windfile.write('Wind Gust ' + windgust + 'MPH' + '\n')
        	windfile.write('Rain Total: ' + rain + 'in')

        #print("Rain Total=\t%0.2f in")%(totalRain)
        #print("Wind Speed=\t%0.2f knots")%(currentWindSpeed)
        #print("MPH wind_gust=\t%0.2f MPH")%(currentWindGust)                                                           

        #print "Wind Direction=\t\t\t %0.2f Degrees" % weatherStation.current_wind_direction()
        #print "Wind Direction Voltage=\t\t %0.3f V" % weatherStation.current_wind_direction_voltage()

	time.sleep(10.0)
