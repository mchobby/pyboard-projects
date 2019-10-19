from pyb import Switch
from machine import Pin, I2C
from time import sleep
from ws2812 import NeoPixel
from tcs34725 import TCS34725

# Pyboard - SDA=Y10, SCL=Y9
i2c = I2C(2)

np = NeoPixel( spi_bus=1, led_count=44, intensity=1)
np.fill( (0,128,0) ) # Starting GBR
np.write()

color = TCS34725(i2c)
color.integration_time = 400 # Bigger integration time means collect more data about color
led = Pin( "Y12", Pin.OUT, value=False )
switch = Switch() # Wired on Pin

def gamma_255( x ):
	""" Apply a gamma correction factor for a value in the range 0 - 255 """
	x /= 255
	x = pow(x, 2.5)
	x *= 255
	return int(x) if x < 255 else 255

def gamma_color( color ):
	""" Apply the Gamma correction to a tuple of rgb color.
		Eyes does not sense the color range in a linear way """
	return gamma_255(color[0]), gamma_255(color[1]), gamma_255(color[2])

# Started and ready for operation
sleep( 0.300 )
np.fill( (128,0,0) ) # GRB Started
np.write()
sleep( 0.500 )
np.fill( (0,0,0) ) # switch off
np.write()

# Main loop reading color and printing it every second.
catch_color = False
while True:
	if switch.value():
		catch_color = not( catch_color )
		led.value( catch_color ) # Light the Acquire LED
		sleep( 0.5 )

	if catch_color:
		# Read the color at the sensor
		rgb = color.color_rgb_bytes    # color_rgb_bytes
		np.fill( (rgb[1],rgb[0],rgb[2]) ) # Give it as grb for triple ring
		np.write()
		# Delay for a second and repeat.
	sleep(0.100)
