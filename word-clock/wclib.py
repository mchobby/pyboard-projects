"""
wclib.py - Word Clock Library including functions, panel definition, etc.

* Author(s): Meurisse D. from MCHobby (shop.mchobby.be).

See project source @ https://github.com/mchobby/pyboard-projects/tree/master/word-clock

"""
#
# The MIT License (MIT)
#
# Copyright (c) 2019 Meurisse D. for MC Hobby
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

HOURS = {0:"DOUZE", 1:"UNE" , 2:"DEUX",  3:"TROIS",  4:"QUATRE", 5:"CINQ", 6:"SIX",
         7:"SEPT" , 8:"HUIT", 9:"NEUF", 10:"DIX"  , 11:"ONZE"  }

MINS = { 0: (None,), 5: ("CINQ",), 10: ("DIX",), 15: ("QUART",), 20: ("VINGT",),
         25: ("VINGT-CINQ",), 30: ("ET","DEMI"),
		 35: ("MOINS", "VINGT-CINQ"), 40: ("MOINS","VINGT"),
		 45: ("MOINS", "QUART"), 50: ("MOINS","DIX"), 55: ("MOINS","CINQ") }

PANEL = ["ILNESTOUNER",
		 "DEUXNUTROIS",
		 "QUATREDOUZE",
		 "CINQSIXSEPT",
		 "HUITNEUFDIX",
		 "ONZERHEURES",
		 "MOINSOLEDIX",
		 "ETRQUARTRED",
		 "VINGT-CINQU",
		 "ETSDEMIEPAM"]

def time_to_words( h, m ):
	""" Convert hour (0 to 24) & minutes (0 to 59) to its text equivalent.
		Eg: 15:26 returns ['IL', 'EST', 'TROIS', 'HEURES', 'VINGT-CINQ'] """

	if m>=35:
		h += 1
	_r = ["IL", "EST", HOURS[h%12],'HEURE' if h in (1,13) else 'HEURES' ]
	for item in MINS[ m//5*5 ]:
		if item:
			_r.append( item )
	return _r


def word_pos( word, from_pos=(0,0) ):
	""" Find the position of a word into the Panel.
	    :params word: CAPITAL word to find.
		:return: ( (pos_x,pos_y), (len_x,len_y) ) """
	col  = from_pos[0]
	line = from_pos[1]
	# -- Look on Horizontal Lines
	for _line in range( line, len(PANEL) ):
		start_col = col if _line==line else 0
		try:
			pos = PANEL[_line].index( word, start_col )
			return ( (pos,_line),(len(word),1) )
		except ValueError:
			pass # Not present in the string
	# -- Nothing found? return None
	return None

def letter_pos( letter, from_pos=(0,0) ):
	for _line in range( from_pos[1], len(PANEL) ):
		start_col = from_pos[0] if _line==from_pos[1] else 0
		try:
			pos = PANEL[_line].index( letter, start_col )
			return (pos,_line)
		except ValueError:
			pass # Not present in the string
	return None

def letters_pos( letters, from_pos=(0,0) ):
	""" Find a suite of letter (continuous or not) and returns their coordinate into a list """
	_r = list( [None for i in letters] ) # prepare an empty result [ None, None, None, .... ]

	last_pos = from_pos
	for l in letters:
		xy = letter_pos( l, from_pos=last_pos)
		if xy:
			idx = letters.index( l )
			_r[idx] = xy
			last_pos = xy
	# -- Nothing found? return None
	return _r

def xy_to_idx( pos ):
	# Return the LED index in the strip based on a (x,y) position. x=column, y=line
	lines   = len(PANEL)
	columns = len(PANEL[0]) # should be 11
	if pos[1]%2 == 0: # if y%2 == 0
		return (pos[1]*columns)+pos[0] # Y*11 + X
	return (pos[1]*columns)+(11-1-pos[0]) # Y*11+(11-1-X)
