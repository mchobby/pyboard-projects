"""
word_clock.py - used the RTC time to display it on a word clock.

It will light words like: IL  EST  DOUZE  HEURES  MOINS  VINGT

* Author(s): Meurisse D. from MCHobby (shop.mchobby.be).

See project source @ https://github.com/mchobby/pyboard-projects/tree/master/word-clock
"""

from wclib import *
from ws2812 import NeoPixel
from time import sleep
from colors import colormap_picker_colors as colormap
from random import randint

# Initialize a date structure
from pyb import RTC
rtc = RTC()

# Pyboard NeoPixel( spi_bus=1, led_count=1, intensity=1 ) -> X8
np = NeoPixel( spi_bus=1, led_count=len(PANEL)*len(PANEL[0]) )

# Last displayed
last_words = []

def is_same_words( ls1, ls2 ):
	""" Check if the two lists have the same contents """
	if len(ls1) != len(ls2):
		return False
	for i in range( len(ls1) ):
		if ls1[i] != ls2[i]:
			return False
	# The two contents are the same
	return True

def show_time():
	""" Manage the time display on the panel.
	:returns: true if time had changed since last display, otherwise False. """

	global rtc, np, last_words
	# Get Current time
	dt = rtc.datetime()
	# Returns ['IL', 'EST', 'UNE', 'HEURE', 'MOINS', 'QUART']
	words = time_to_words(dt[4], dt[5])
	if is_same_words( words, last_words ):
		print( "Nothing to update" )
		return False
	last_words = words
	print( "display %2s:%2s -> %s" % (dt[4], dt[5], words) )
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
		color = colormap[randint(0,len(colormap)-1)]
		# Position in the strip LED
		for i in range( _position[1][0] ):
			# attn: pixel are numeroted forward one line on two, backward the
			#       other lines
			pos = xy_to_idx( (_position[0][0]+i,_position[0][1]) )
			np[pos] = color
	np.write()
	return True

# Main loop
while True:
	show_time()
	# waits 30s. So 2 updates per minute
	sleep( 30 )
