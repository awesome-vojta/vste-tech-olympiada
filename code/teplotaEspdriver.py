import urllib2
#import urllib.request
#import urllib.parse
#import re

def readEsp():
    url = urllib2.urlopen("http://192.168.1.9/?pin=TEPLOTA!")
    values = url.read()
    words = values.split("DS_temp=")
    teplota = words[-1]
    return "{0:.2f}".format(convertToNumber(teplota))
