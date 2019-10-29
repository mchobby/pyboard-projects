from ad9833 import AD9833, MODE_SINE
from machine import Pin, SPI

# Notes = Key,Frequency
# 523.25, 587.33, 659.26, 698.46, 783.99, 880, 987.77, 1046.50
NOTES = { 'C':523, 'D': 587, 'E':659, 'F':698, 'G':784, 'A':880, 'B':988, 'C': 1046 }

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
		# Find a free oscillator and play the note
		# If no oscillator available --> do nothing
		for _voice in self.voices:
			if not(_voice.note):
				_voice.note = note
				_voice.generator.freq = NOTES[note]
				_voice.reset = False # Release the signal generator
				self.debug( "Play note %s on %s" % (note,_voice.generator.fsync.names()[1]) )
				break

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

# Create SPI bus for AD9833
spi = SPI(2, polarity=1, phase=0)

# create organ & add voices
organ = Organ( spi=spi, debug=True )
organ.add_voice( "Y5" )
organ.add_voice( "Y4" )

organ.clear_all()
