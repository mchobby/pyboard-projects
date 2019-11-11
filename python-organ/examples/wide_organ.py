"""
Wide-Organ - The MicroPython polyphonic Organ project over 2 octaves and 4 AD9833 frequence generator.

* Author(s): Meurisse D. from MCHobby (shop.mchobby.be).

See project source @ https://github.com/mchobby/pyboard-projects/tree/master/python-organ

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


from ad9833 import AD9833, MODE_SINE
from mpr121 import MPR121
from machine import Pin, SPI, I2C
from time import sleep

green_btn  = Pin( "X5", Pin.IN, Pin.PULL_UP )
red_btn    = Pin( "X6", Pin.IN, Pin.PULL_UP )
yellow_btn = Pin( "X7", Pin.IN, Pin.PULL_UP )
blue_btn   = Pin( "X8", Pin.IN, Pin.PULL_UP )

# Notes = Key,Frequency
# 523.25, 587.33, 659.26, 698.46, 783.99, 880, 987.77, 1046.50
NOTES = { 'C1':523  , 'D1': 587, 'E1': 659, 'F1': 698, 'G1': 784, 'A1': 880, 'B1': 988,
		  'C2': 1046, 'D2':1110, 'E2':1182, 'F2':1221, 'G2':1307, 'A2':1403, 'B2':1511,
		  'C3': 1569 }
# Keys = correspondance between KEY index and corresponding note
KEYS = ['C1','D1','E1','F1','G1','A1', 'B1', 'C2', 'D2', 'E2', 'F2', 'G2', 'A2', 'B2', 'C3']

class Voice:
	""" store information about a voice (an AD9833) and current note. """
	generator = None  # AD9833 reference (includes its FSYNC (ss) Pin reference
	note     = None   # Current note None or note Letter

class Organ:
	def __init__( self, spi, debug=False ):
		self.voices = []
		self.spi = spi
		self._debug = debug

	def add_voice( self, ss_pinname ):
		""" Add a AD9833 generator as voice.
		:param ss_pinname: name of the SSPin to contrôle the AD9833 """
		self.debug( "Adding voice on FSYNC pin %s" % ss_pinname )
		_voice = Voice()
		_voice.generator = AD9833( spi=self.spi, fsync_pin=Pin(ss_pinname, Pin.OUT, value=1) )
		# Configure Freq0 @ 0 Hz
		_voice.generator.select_register(0)
		_voice.generator.mode = MODE_SINE
		_voice.generator.freq = 0
		_voice.generator.phase = 0
		_voice.generator.reset = True # On Hold
		# Current note = None
		_voice.note      = None
		self.voices.append( _voice )

	def debug( self, msg ):
		# display debug message
		if self._debug:
			print( msg )

	def clear_all( self ):
		# palce all oscillator "On Hold"
		for _voice in self.voices:
			_voice.generator.reset=True
			_voice.note = None

	def play_note( self, note ):
		assert note in NOTES, 'Invalid note %s' % note
		# Do not play twice the same note
		if note in self.playing_status():
			self.debug( "Note %s already playing!" % note )
			return
		# Find a free oscillator and play the note
		# If no oscillator available --> do nothing
		for _voice in self.voices:
			if not(_voice.note):
				_voice.note = note
				_voice.generator.select_register(0)
				_voice.generator.mode = MODE_SINE
				_voice.generator.freq = NOTES[note]
				_voice.generator.phase= 0  # No phase shift (0..4095)
				_voice.generator.reset = False # Release the signal generator
				self.debug( "Play note %s on %s @ %s Hz" % (note,_voice.generator.fsync.names()[1],NOTES[note]) )
				return
		self.debug( "No voice remaining!")

	def clear_note( self, note ):
		# Find the oscillator that play the note
		# If not found --> do nothing
		for _voice in self.voices:
			if _voice.note == note:
				_voice.generator.reset = True # generator "on hold"
				_voice.note = None
				self.debug( "Clear note %s on %s" % (note,_voice.generator.fsync.names()[1]) )
				break

	def playing_status( self ):
		""" list of voices with note currently playing """
		return [_voice.note for _voice in self.voices ]

class Keyboard():
	""" MPR121 Keyboard based on ONE or Several MPR121 """
	def __init__(self, i2c, addrs = [0x5A], debug=False):
		self.MPRs = list()
		for addr in addrs:
			self.MPRs.append( MPR121( i2c, address=addr ) )
		self.touched = bytearray( self.reader_count*12*2 ) # Allow to read twice the states and store it in store1 or store2 µ

		self._debug = debug
		# Initialize the touched
		self.read( store=1 ) # Current state
		self.read( store=2 ) # Last Known state
		# Callback routine
		self.on_key_change = None # Annonce Pressed/Release with callback( key=0..12, Pressed=True ) otherwise it callit for release

	def debug( self, msg ):
		# display debug message
		if self._debug:
			print( msg )

	@property
	def reader_count( self ):
		""" Number of MPR121 reader (of 12 entries each) """
		return len( self.MPRs )

	def read( self, store ):
		""" Read and decode touched entries and populate touched store """
		assert 1<=store<=2, "Can only read data to store 1 or 2"
		z = zip( range(self.reader_count), self.MPRs )
		for mpr_index, mpr in z:
			data = mpr.touched()
			for i in range( 12 ):
				self.touched[(mpr_index*12)+(i+(store-1)*12)] = 1 if data & (1<<i) else 0

	def update( self ):
		""" Call it as often as possible to detect key pressed / key released """
		# Read the current state
		self.read( store=1 )
		for key in range( self.reader_count * 12 ):
			# Key state has changed? (pressed or release)
			if self.touched[key] != self.touched[key+(self.reader_count*12)]:
				self.debug( "Key %i is %s" %(key,"PRESSED" if self.touched[key]>0 else "Released") )
				if self.on_key_change:
					self.on_key_change( key, pressed=(self.touched[key]>0) )
				# remember the current state as last state
				self.touched[key+(self.reader_count*12)]=self.touched[key]


# Create SPI bus for AD9833
spi = SPI(2, baudrate=9600, polarity=1, phase=0)
i2c = I2C(2)

# create organ & add voices
organ = Organ( spi=spi, debug=True )
organ.add_voice( "Y2" ) # Add or remove depending on available voices
organ.add_voice( "Y3" )
organ.add_voice( "Y4" )
organ.add_voice( "Y5" )
organ.clear_all()

def keyboard_changed( key, pressed ):
	""" This will be called when a key is pressed or released """
	global organ
	# Key from 0 to 7 are for corresponding notes in NOTES
	if 0<= key < len(KEYS):
		# Transform key index into Note letter
		note = KEYS[key]
		if pressed:
			organ.play_note(note)
		else:
			organ.clear_note(note)

# Create the keyboard
keyb=Keyboard( i2c=i2c, addrs = [0x5A,0X5B], debug=False )
keyb.on_key_change = keyboard_changed
while True:
	keyb.update()
	if blue_btn.value()==0:
		print( "Resetting..." )
		organ.clear_all()
		organ.play_note('C2')
		sleep(0.5)
		organ.clear_note('C2')
		sleep(0.5)
		organ.play_note('C2')
		sleep(0.5)
		organ.clear_note('C2')
		sleep(0.5)
		print( "Reset done" )
