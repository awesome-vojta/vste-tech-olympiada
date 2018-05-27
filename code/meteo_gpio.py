#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2, time, datetime, os
import RPi.GPIO as GPIO
import ds18b20driver
import dht11driver
import dht22driver
import bh1750fvidriver
import teplotaEspdriver
import BMP085driver
#import meteo_gpio
#from meteo_gpio import *

#config
DHT11_PIN = 24
DHT22_PIN = 14
PIR_PIN = 21

#variables
temperature1 = 0
humidity1 = 0
temperature2 = 0
humidity2 = 0
light = 0

def readTemperatureIN():
	global DHT11_PIN, temperature1, humidity1
	try:
		count = 0
		while True:
		  dht11var = dht11driver.DHT11(pin = DHT11_PIN)
		  result = dht11var.read()
		  if result.is_valid():
			temperature1 = int(result.temperature)
			humidity1 = int(result.humidity)
			#print "Vlhkost "+str(humidity) + " %" + ", teplota " + str(result.temperature) + " °C"
			return True
			break
		  count += 1
		  if count>10:
			return False
			break
		  time.sleep(1)
	except:
		return False

def readTemperatureOUT():
	global temperature2
	try:
		basedir = '/sys/bus/w1/devices'
		sensors = ds18b20driver.find_sensors(basedir)
		if not sensors:
			#print "senzor ds18b20 nedetekován"
			return False
		for s in sensors:
			(ok, temp) = ds18b20driver.read_temp(basedir + '/' + s)
			if ok:
				teplota = float("{0:.2f}".format(temp / 1000.0))
				temperature2 = int(teplota)
				return True
				break
	except:
		return False
	
def readHumidityOUT():
	global DHT22_PIN, humidity2
	try:
		count = 0
		while True:
		  t, h, ok = dht22driver.read(DHT22_PIN)
		  if ok:
				humidity2 = int(h)
				#print "Vlhkost "+str(h) + " %" + ", teplota " + str(t) + " °C"
				return True
				break
		  count += 1
		  if count>10:
			return False
			break
		  time.sleep(1)
	except:
		return False

def readEsp():
	global teplotaEsp
	try:
		teplotaEsp = teplotaEspdriver.readEsp()
		return True
	except:
		return False

def readPress():
	global pressure
	try:
		pressure = BMP085driver.read_pressure()
		return True
	except:
		return False
		
def readAltitude():
	global altitude
	try:
		altitude = BMP085driver.read_altitude()
		return True
	except:
		return False

def readLight():
	global light
	try:
		light = bh1750fvidriver.readLight()
		return True
	except:
		return False

def display_backlight_on(*args):
  #Turn on backlight
  os.system("echo 0 | sudo tee /sys/class/backlight/*/bl_power")
  os.system("xset s reset && xset dpms force on")
  #Turn off backlight
  #echo 1 | sudo tee /sys/class/backlight/*/bl_power


# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
GPIO.setup(PIR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=display_backlight_on, bouncetime=300)
#os.popen("sudo i2cset -y -r  1 0x70 0xff")
