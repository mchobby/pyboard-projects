"""
servo90.py - Pythonic Boris Servo Calibration
Activate the PCA985 servos (output 0 to 6) at 90°.

* Author(s): Meurisse D. from MCHobby (shop.mchobby.be).

See project source @ https://github.com/mchobby/pyboard-projects/tree/master/pythonic-boris
"""
from machine import I2C
from time import sleep_ms

# Import ServoCtrl, classe pour le controleur PMW
from servoctrl import ServoCtrl

# I2C Bus on Y9,Y10
i2c = I2C( 2 )

# Create the PWM controler object (default address 0x40)
# Angles are from 0 to 180°)
servos = ServoCtrl( i2c )

try:
	print( "Set servo[0..5] @ 90 degres")
	# Set the Boris LEGS servos at their calibration position (90° = the middle between 0 & 180°)
	for i in range( 0, 6 ):
		# 90° le servo moteur #15 à un angle de 45 degrés
		servos.position( i, 90 )
	print( "Press Ctrl+C to exit")
	while True:
		sleep_ms( 10 )
except KeyboardInterrupt:
	for i in range( 0,6 ):
		servos.release()
	print("All servo released!")

print( "That s all folks!")
