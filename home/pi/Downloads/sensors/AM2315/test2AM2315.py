import time
from tentacle_pi.AM2315 import AM2315
am = AM2315(0x5c,"/dev/i2c-1")


#!/usr/bin/env python




for x in range(0,2):
    temperature, humidity, crc_check = am.sense()
    Fahrenheit = 9.0/5.0 * temperature + 32
    print "temperature: %0.1f""F" % Fahrenheit
    print "temperature: %0.1f""C" % temperature
    print "humidity: %0.1f%%" % humidity
    print
    time.sleep(2.0)



#    print "temperature: %0.1f" % temperature

#    print "crc: %s" % crc_check


#Celsius = "temperature: %0.1f"




#print "Temperature:", Celsius, "Celsius = ", Fahrenheit, " F"