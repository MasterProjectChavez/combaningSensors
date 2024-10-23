
import RPi.GPIO as GPIO
import time

thisPin=11 #Override with input from setup

def setup(passivePin): # Sets up Passive buzzer
    thisPin=passivePin
    GPIO.setmode(GPIO.BOARD)		# Numbers GPIOs by physical location
    GPIO.setup(passivePin, GPIO.OUT)	# Set pins' mode is output
    global Buzz						# Assign a global variable to replace GPIO.PWM 
    Buzz = GPIO.PWM(passivePin, 440)	# 440 is initial frequency.
    Buzz.start(50)					# Start Buzzer pin with 50% duty ration

def stop():
    Buzz.stop()
    GPIO.output(thisPin, 1)		# Set passive Buzzer pin to High