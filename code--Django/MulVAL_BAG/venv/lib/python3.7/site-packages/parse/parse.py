# -*- coding: utf-8 -*-
"""
Created on Wed May 08 16:11:28 2013

@author: kshmirko
"""
import re
from ios.readMeteoBlock import readMeteoFile, readMeteoCtx
import StringIO

from datetime import datetime, timedelta

class ParserException(Exception):
    def __init__(self, text):
        super(ParserException, self).__init__(text)

regex = re.compile("(?P<stid>[0-9]+)([a-zA-Z\ \(\)]+)(?P<time>[0-9]+\w\ [0-9]+\ \w+\ [0-9]+)",re.IGNORECASE|re.UNICODE|re.DOTALL)


def parse_h2(line):
    print line
    r = regex.match(line).groupdict()
    
    stid = int(r['stid'])
    date = datetime.strptime(r['time'],'%HZ %d %b %Y')
    print stid, date
    return stid, date

def parse_pre1(line):
    sfile = StringIO.StringIO(line)
    meteo = readMeteoFile(sfile)
    return meteo
    
def parse_pre2(line):
    sfile = StringIO.StringIO(line)
    ctx = readMeteoCtx(sfile)    
    return ctx

def parse_h3(line):
    pass
    
def parse_observation(tags):
    tmp = tags.pop()
    if tmp.tag=='h2':
        print "Header OK"
        stid, date = parse_h2(tmp.text)
    else:
        raise ParserException("Can't parse string '%s'\n"%(tmp.text))

    tmp = tags.pop()
    if tmp.tag=='pre':
        print "data OK"
        meteo = parse_pre1(tmp.text)
    else:
        raise ParserException("Can't parse string '%s'\n"%(tmp.text))
        
    tmp = tags.pop()
    if tmp.tag=='h3':
        print "Indices title OK"
        parse_h3(tmp.text)
    else:
        raise ParserException("Can't parse string '%s'\n"%(tmp.text))
        
    tmp = tags.pop()
    if tmp.tag=='pre':
        print "Indices OK"
        ctx = parse_pre2(tmp.text)
    else:
        raise ParserException("Can't parse string '%s'\n"%(tmp.text))
    
    
    return [stid, date, meteo, ctx]