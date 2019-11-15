"""
test_pixelwords.py - test translation from clock (h:m) to words THEN words to NeoPixels

EG: 23:40 -> ['IL', 'EST', 'DOUZE', 'HEURES', 'MOINS', 'VINGT']

* Author(s): Meurisse D. from MCHobby (shop.mchobby.be).

See project source @ https://github.com/mchobby/pyboard-projects/tree/master/word-clock

"""
from wclib import *
from ws2812 import NeoPixel
from time import sleep

# Pyboard NeoPixel( spi_bus=1, led_count=1, intensity=1 ) -> X8
np = NeoPixel( spi_bus=1, led_count=len(PANEL)*len(PANEL[0]) )

# Initialize a date structure
from pyb import RTC


def show_time( hours, mins ): # 0 to 24 Hours, 0 to 59 mins
	""" Light up the proper LEDs on the clock """
	words = time_to_words(hours, mins)
	print( "%2s:%2s -> %s" % ( hours, mins, words) )


	# Where are words in the PANEL
	_positions = [] # List of positions to light
	start_pos = (0,0)
	for word in words:
		# Position of the word on the matrix
		pos = word_pos( word, start_pos )
		_positions.append( pos )
		print( "    %s located @ %s" % (word,pos) )
		if word in ("HEURE","HEURES"):
			start_pos = pos[0] # Can only search the word after "HEURE"

	# Light Up the position
	print( "Lighting up PANEL" )
	np.fill( (0,0,0) )
	for _position in _positions:
		# HEURE located @ ((5, 5), (5, 1)) = ( (x_pos,y_pos),(x_len,y_len) )
		print( "    light up @",  _position )
		# Position in the strip LED
		for i in range( _position[1][0] ):
			# attn: pixel are numeroted forward one line on two, backward the
			#       other lines
			pos = xy_to_idx( (_position[0][0]+i,_position[0][1]) )
			np[pos] = (0,0,255)
	np.write()


def run():
	# Main Loop
	rtc = RTC()
	dt = rtc.datetime()
	delta_min = 3 # increment by 3 minutes
	total_min = 0
	while total_min < 1440: # up to 24H
		show_time( dt[4], dt[5] )
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

		# Wait a bit
		sleep( 0.2 )

run()
print( "That's all folks!")
