#!/usr/bin/env python

print("Content-Type: text/plain\n\n")
print("hello")

import sys
import Adafruit_DHT
import Adafruit_BMP.BMP085 as BMP085


#BMP180
#sensor = BMP085.BMP085(mode=BMP085.BMP085_ULTRAHIGHRES)

#temperature = sensor.read_temperature()
#pressure = sensor.read_pressure()
#print "--- BMP180 ---"
#print "Temperature: %+.1f C" % temperature
#print "Pressure = %.2f hPa" % pressure



#AM2315
from tentacle_pi.AM2315 import AM2315
am = AM2315(0x5c,"/dev/i2c-1")

temperature, humidity, crc_check = am.sense()

Fahrenheit = 9.0/5.0 * temperature + 32
print "--- AM2315 ---"
print "temperature: %0.1f""F" % Fahrenheit
print "temperature: %0.1f""C" % temperature
print "humidity: %0.1f%%" % humidity


#Wind&Rain
#sys.path.append('./Adafruit_ADS1x15')
#import SDL_Pi_Weather_80422 as SDL_Pi_Weather_80422

#anenometerPin = 23
#rainPin = 24
#SDL_MODE_INTERNAL_AD = 0
#SDL_MODE_I2C_ADS1015 = 1

#sample mode means return immediately.  The wind speed is averaged at sampleTime or when you ask, whichever is longer
#SDL_MODE_SAMPLE = 0
#Delay mode means to wait for sampleTime and the average after that time.
#SDL_MODE_DELAY = 1

#weatherStation = SDL_Pi_Weather_80422.SDL_Pi_Weather_80422(anenometerPin, rainPin, 0,0, SDL_MODE_I2C_ADS1015)

#weatherStation.setWindMode(SDL_MODE_SAMPLE, 5.0)
#weatherStation.setWindMode(SDL_MODE_DELAY, 5.0)

#totalRain = 0

#while True:

#currentWindSpeed = weatherStation.current_wind_speed()/1.6
#currentWindGust = weatherStation.get_wind_gust()/1.6
#totalRain = totalRain + weatherStation.get_current_rain_total()/25.4
#print("Rain Total=\t%0.2f in")%(totalRain)
#print "--- Wind & Rain ---"
#print("Wind Speed=\t%0.2f MPH")%(currentWindSpeed)
#print("MPH wind_gust=\t%0.2f MPH")%(currentWindGust)

#print "Wind Direction=\t\t\t %0.2f Degrees" % weatherStation.current_wind_direction()
#print "Wind Direction Voltage=\t\t %0.3f V" % weatherStation.current_wind_direction_voltage()

#time.sleep(3.0)


