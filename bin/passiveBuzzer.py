
import RPi.GPIO as GPIO
import time
def setupPassive(passivePin): # Sets up Passive buzzer
    GPIO.setmode(GPIO.BOARD)		# Numbers GPIOs by physical location
    GPIO.setup(passivePin, GPIO.OUT)	# Set pins' mode is output
    global Buzz						# Assign a global variable to replace GPIO.PWM 
    Buzz = GPIO.PWM(passivePin, 440)	# 440 is initial frequency.
    Buzz.start(50)					# Start Buzzer pin with 50% duty ration
      