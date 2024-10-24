#!/usr/bin/env python3
import RPi.GPIO as GPIO
import combined
import activeBuzzer

BtnPin = 11
Gpin   = 12
Rpin   = 13
type=-1


def setup(buttonPin, localGpin, localRpin, thisType):
	BtnPin=buttonPin
	Gpin=localGpin
	Rpin=localRpin
	type=thisType #0=increase temperature button, 1=decrease temperature button
	#GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
	GPIO.setup(Gpin, GPIO.OUT)     # Set Green Led Pin mode to output
	GPIO.setup(Rpin, GPIO.OUT)     # Set Red Led Pin mode to output
	GPIO.setup(BtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Set BtnPin's mode is input, and pull up to high level(3.3V)
	GPIO.add_event_detect(BtnPin, GPIO.BOTH, callback=detect, bouncetime=200)

def Led(x):
	if x == 0:
		GPIO.output(Rpin, 1)
		GPIO.output(Gpin, 0)
	if x == 1:
		GPIO.output(Rpin, 0)
		GPIO.output(Gpin, 1)
	if type==1:
		combined.Temperature+=1
	elif type==0:
		combined.Temperature-=1
	activeBuzzer.beep()

def detect(chn):
	Led(GPIO.input(BtnPin))
	return True

def loop():
	while True:
		pass

def destroy():
	GPIO.output(Gpin, GPIO.HIGH)       # Green led off
	GPIO.output(Rpin, GPIO.HIGH)       # Red led off
	GPIO.cleanup()                     # Release resource

if __name__ == '__main__':     # Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()

