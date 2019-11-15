"""
test_allblue.py - set all the pixels to BLUE to check power and data wiring

* Author(s): Meurisse D. from MCHobby (shop.mchobby.be).

See project source @ https://github.com/mchobby/pyboard-projects/tree/master/word-clock

"""

from wclib import *
from ws2812 import NeoPixel

# Pyboard NeoPixel( spi_bus=1, led_count=1, intensity=1 ) -> X8
np = NeoPixel( spi_bus=1, led_count=len(PANEL)*len(PANEL[0]) )
np.fill( (0,0,255) )
np.write()
