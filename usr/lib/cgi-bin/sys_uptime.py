#!/usr/bin/python

from datetime import timedelta
from datetime import datetime

with open('/proc/uptime', 'r') as f:
    uptime_seconds = float(f.readline().split()[0])
    uptime_string = str(timedelta(seconds = uptime_seconds))
    #uptime_string = int(uptime_string)

#'{:%Y-%m-%d %H:%M}'.format(datetime(uptime_string))

print (uptime_string)