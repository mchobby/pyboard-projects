# Create a polyphonic organ with sinus generators, capactive sensor and MicroPython

![Python-Organ](docs/_static/python-organ-logo.jpg)

Create a nice polyphonic instrument with SPI based oscillator.

![Python-Organ](docs/_static/Python-Organ-(640px).jpg)

Based on the "__Penny Organ__" Arduino project from Julian Ilett (see [this Youtube vidéo](https://youtu.be/2PehLon9X5k))

# Wiring

An external 5V jack is placed on the schematic to allow powering the organ with 5V wall PSU when development is finished.

![Wiring the Python-Organ (part 1)](docs/_static/python-organ-ad9833.jpg)

![Wiring the Python-Organ (part 2)](docs/_static/python-organ-audio.jpg)

![Python-Organ MPR121 key assignation](docs/_static/mpr121_notes.jpg)

__During development phase:__
* The 5V power should be removed from VDD pin (on amplifier) which allow the python-organ to be powered via the USB (without powering the amplifier which is current hungry).
* Amplifier can still be powered separately from its own Power Jack (__only if vdd has been removed!__)

# Dependencies
This project relies on the following library
* ad9833.py : sinus signal generator library [located here (esp8266-upy GitHub)](https://github.com/mchobby/esp8266-upy/tree/master/ad9833)
* mpr121.py : 12 keys capacitive sensor [located here (esp8266-upy GitHub)](https://github.com/mchobby/esp8266-upy/tree/master/mpr121)

# Videos
* [Hardware & audio presentation](https://youtu.be/CDhU_MLfy3o) (_YouTube,French_)

# Running

## Basic example
Just run the script `python_organ.py` (or rename it as `main.py`).

`python_organ.py` use only one MPR121 breakout for 8 notes (one octave).

## Advanced example (Maker Faire)

The `examples/wide_organ.py` is the Maker Faire setup using 2x MPR121 breakouts for 15 notes (two octaves) and 4 signal generator (4 voices).

Just run the script `wide_organ.py` (or rename it as `main.py`).


# Shopping list
* [Pyboard original](https://shop.mchobby.be/fr/micropython/570-micropython-pyboard-3232100005709.html) @ MCHobby.be
* [MPR121 breakout](https://shop.mchobby.be/fr/tactile-flex-pot-softpad/1685-capteur-capacitif-12-touches-mpr121-3232100016859-adafruit.html) @ MCHobby.be
* [AD9833 signal generator breakout](https://shop.mchobby.be/fr/breakout/1689-generateur-de-signal-sinus-triangle-clock-0-125-mhz-3232100016897.html) @ MCHobby.be
