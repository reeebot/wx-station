#!/usr/bin/env python
#-*- coding: utf-8 -*-

import time
import sys
import urllib2
import os

import random
from retrying import retry

os.chdir("/usr/lib/cgi-bin")

@retry(wait_fixed=2000)
def upload():
	while True:
		#IMPORT DATA TXT FILES
		wind_ = open("/usr/lib/cgi-bin/winddata.txt", 'r', os.O_NONBLOCK).read().split()
		temp_ = open("/usr/lib/cgi-bin/tempdata.txt", 'r', os.O_NONBLOCK).read().split()


		#SEND TO WU
		urlWU = "http://rtupdate.wunderground.com/weatherstation/updateweatherstation.php?ID=KCOFORTC162&PASSWORD=hilltopWx&dateutc=now&tempf={0}&dewptf={1}&humidity={2}&baromin={3}&winddir={4}&windspeedmph={5}&action=updateraw&realtime=1&rtfreq=5".format(temp_[0],temp_[1],temp_[2],temp_[3],wind_[0],wind_[1],wind_[2])
		urllib2.urlopen(urlWU).read() #send data to Weather Underground

		time.sleep(5.5)

upload()
