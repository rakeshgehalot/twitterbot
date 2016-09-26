#!/usr/bin/env python

import time
import random
import tweepy
import RPi.GPIO as GPIO
from urllib2 import urlopen
from contextlib import closing
import json


sw = 15
led1 = 14
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(sw, GPIO.IN)
GPIO.setup(led1, GPIO.OUT)


from twython import TwythonStreamer
url = 'http://freegeoip.net/json/'
TERMS = 'crystalx'

APP_KEY = "your_key"
APP_SECRET = "your_key"
OAUTH_TOKEN = "your_key"
OAUTH_TOKEN_SECRET = "your_key"

auth = tweepy.OAuthHandler(APP_KEY, APP_SECRET)
auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
api = tweepy.API(auth)


class BlinkyStreamer(TwythonStreamer):
        def on_success(self, data):
                if 'text' in data:                        
			twe = data['text'].encode('utf-8')
			if 'name' in twe:
				api.update_status(status="My name is Crystal-X and Rakesh is my Inventor. %d" % (random.randint(0,500),))
				print twe
				
			elif 'temperature' in twe:	
				
				if GPIO.input(sw):
					api.update_status(status="Here at Jupiter the weather is not good it's very COLD. %d" % (random.randint(0,500),))
					print "led is OFF"
				else:
					api.update_status(status="Here at Jupiter the weather is not good it's very HOT. %d" % (random.randint(0,500),))	
					print "led is ON"
			elif 'what do' in twe:	
 				api.update_status(status="I am here at Jupiter to make space station for Rakesh. %d" % (random.randint(0,500),))
 				print twe
 			elif 'ON' in twe:
 				GPIO.output(led1,GPIO.HIGH)	
 				api.update_status(status="I Turned ON the Camera1 on Jupiter Rakesh. %d" % (random.randint(0,500),))
 				print twe
 			elif 'OFF' in twe:
 				GPIO.output(led1,GPIO.LOW)	
 				api.update_status(status="I Turned OFF the Camera1 on Jupiter Rakesh. %d" % (random.randint(0,500),))
 				print twe
 			elif 'location' in twe:
 				with closing(urlopen(url)) as response:
        				location = json.loads(response.read())
        				loc =location['city'].encode('utf-8') + ' ' + location['region_name'].encode('utf-8')+ ' ' + location['ip'].encode('utf-8') + ' ' + location['country_name'].encode('utf-8')
        				loc2  = location['longitude'], location['latitude']
        				rn = random.randint(0,500)
				        loc3 = loc , loc2, rn
 				api.update_status(loc3)
 				print twe		
 
try:
        stream = BlinkyStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
        stream.statuses.filter(track=TERMS)
except KeyboardInterrupt:
	GPIO.cleanup()
        print "\n\n        *** Get Lost *** \n\n"
