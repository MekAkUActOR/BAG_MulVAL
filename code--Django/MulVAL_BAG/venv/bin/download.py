# -*- coding: utf-8 -*-
"""
Created on Wed May 08 14:53:52 2013

@author: kshmirko
"""

import lxml.html
import urllib
import sys
import os

def readini():
    fname, url = None,None
    
    with open('meteo.ini','rt') as f:
	while f.tell() < os.path.getsize('meteo.ini'):
	    fname = f.readline().strip()
	    url = f.readline().strip()
	    yield (fname, url)


from parse.parse import parse_observation, ParserException
from ncfile.meteofile import meteoFile

data=None

for item in readini():
    ncname, url = item
#with open('meteo.html') as f:
#    data = f.read()

    data = urllib.urlopen(url).read()



    doc = lxml.html.document_fromstring(data)

    body = doc.xpath('/html/body')[0]

# select all tags under body
    children = [ item for item in body.iterchildren() ]
    children.reverse()
    f=meteoFile(ncname)
    f.initfile()
    try:
	# Parse output while the input isn't empty
	while True:
    	    data = parse_observation(children)
    	    f.add(data)
    except ParserException, e:
	sys.stderr.write('\n\nError! %s'%e)
	sys.stderr.flush()

    f.writedown()