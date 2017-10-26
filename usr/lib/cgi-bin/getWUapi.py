#!/usr/bin/env python
#-*- coding: utf-8 -*-

import time
import sys
import urllib2
import json


#GET WU API
f = urllib2.urlopen('http://api.wunderground.com/api/a72376c63fc5cb55/geolookup/conditions/q/IA/Cedar_Rapids.json')
json_string = f.read()
parsed_json = json.loads(json_string)
location = parsed_json['location']['city']
temp_f = parsed_json['current_observation']['temp_f']
print "Current temperature in %s is: %s" % (location, temp_f)
f.close()
