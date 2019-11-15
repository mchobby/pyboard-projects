"""
test_wording.py - test translation from clock (h:m) to words.

EG: 23:40 -> ['IL', 'EST', 'DOUZE', 'HEURES', 'MOINS', 'VINGT']

* Author(s): Meurisse D. from MCHobby (shop.mchobby.be).

See project source @ https://github.com/mchobby/pyboard-projects/tree/master/word-clock

"""
from wclib import *

# Initialize a date structure
from pyb import RTC
rtc = RTC()
dt = rtc.datetime()

delta_min = 3 # increment by 3 minutes
total_min = 0
while total_min < 1440: # up to 24H
	words = time_to_words(dt[4], dt[5])
	print( "%2s:%2s -> %s" % ( dt[4], dt[5], words) )
	total_min = total_min + delta_min
	# Add minutes to date
	_l = list( dt ) # Tuple to list (because tuple are immutable)
	_l[5] += 3
	if _l[5]>59:
		_l[4] += 1
		_l[5] = _l[5]-59
	if _l[4]>23:
		_l[4] = 0
	dt = tuple( _l ) # List to tuple

print( "That's all folks!")
