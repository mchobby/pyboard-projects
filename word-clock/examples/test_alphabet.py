"""
Check the presence of alphabet letter in the Panel definition.

* Author(s): Meurisse D. from MCHobby (shop.mchobby.be).

See project source @ https://github.com/mchobby/pyboard-projects/tree/master/word-clock

"""
from wclib import *

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ*/-+"

for c in alphabet:
	print( "%s is %s" % (c, 'present' if letter_pos( c ) else 'ABSENT') )

print( "That's all folks")
