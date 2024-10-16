#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

#Buzzers Setup
Buzzer = 11

#Button setup
BtnPin = 11
Gpin   = 12
Rpin   = 13

Temperature=70 #Default temperature of sensor is 70 degrees Fahrenheit

CL = [0, 131, 147, 165, 175, 196, 211, 248]		# Frequency of Low C notes

CM = [0, 262, 294, 330, 350, 393, 441, 495]		# Frequency of Middle C notes

CH = [0, 525, 589, 661, 700, 786, 882, 990]		# Frequency of High C notes
""" Deprecated code
song_1 = [	CM[3], CM[5], CM[6], CM[3], CM[2], CM[3], CM[5], CM[6], # Notes of song1
            CH[1], CM[6], CM[5], CM[1], CM[3], CM[2], CM[2], CM[3], 
            CM[5], CM[2], CM[3], CM[3], CL[6], CL[6], CL[6], CM[1],
            CM[2], CM[3], CM[2], CL[7], CL[6], CM[1], CL[5]	]

beat_1 = [	1, 1, 3, 1, 1, 3, 1, 1, 			# Beats of song 1, 1 means 1/8 beats
            1, 1, 1, 1, 1, 1, 3, 1, 
            1, 3, 1, 1, 1, 1, 1, 1, 
            1, 2, 1, 1, 1, 1, 1, 1, 
            1, 1, 3	]

song_2 = [	CM[1], CM[1], CM[1], CL[5], CM[3], CM[3], CM[3], CM[1], # Notes of song2
            CM[1], CM[3], CM[5], CM[5], CM[4], CM[3], CM[2], CM[2], 
            CM[3], CM[4], CM[4], CM[3], CM[2], CM[3], CM[1], CM[1], 
            CM[3], CM[2], CL[5], CL[7], CM[2], CM[1]	]

beat_2 = [	1, 1, 2, 2, 1, 1, 2, 2, 			# Beats of song 2, 1 means 1/8 beats
            1, 1, 2, 2, 1, 1, 3, 1, 
            1, 2, 2, 1, 1, 2, 2, 1, 
            1, 2, 2, 1, 1, 3 ]
"""

def setup(): # Sets up Passive buzzer
    GPIO.setmode(GPIO.BOARD)		# Numbers GPIOs by physical location
    GPIO.setup(Buzzer, GPIO.OUT)	# Set pins' mode is output
    global Buzz						# Assign a global variable to replace GPIO.PWM 
    Buzz = GPIO.PWM(Buzzer, 440)	# 440 is initial frequency.
    Buzz.start(50)					# Start Buzzer pin with 50% duty ration
    
    #Sets up Ultrasonic sensor
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    
    
def setup(pin):#Sets up Active buzzer
    global BuzzerPin
    BuzzerPin = pin
    GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
    GPIO.setup(BuzzerPin, GPIO.OUT)
    GPIO.output(BuzzerPin, GPIO.HIGH)
    
    
def on(): #Turns Active Buzzer on
    GPIO.output(BuzzerPin, GPIO.LOW)

def off(): #TUrns Active Buzzer off
    GPIO.output(BuzzerPin, GPIO.HIGH)
    
def beep(x): #Prompts the active buzzer to beep
    on()
    time.sleep(x)
    off()
    time.sleep(x)

def loop(): #Normal behavior
    """ Deprecated code
    while True:
        #    Playing song 1...
        for i in range(1, len(song_1)):		# Play song 1
            Buzz.ChangeFrequency(song_1[i])	# Change the frequency along the song note
            time.sleep(beat_1[i] * 0.5)		# delay a note for beat * 0.5s
        time.sleep(1)						# Wait a second for next song.

        #    Playing song 2...
        for i in range(1, len(song_2)):     # Play song 1
            Buzz.ChangeFrequency(song_2[i]) # Change the frequency along the song note
            time.sleep(beat_2[i] * 0.5)     # delay a note for beat * 0.5s
    """
    standby=True;
    while standby: #Keeps the ultrasonic sensor on standby when nobody is within 50 cm of the thermostat
        dis = distance()
        print (dis, 'cm')
        print ('')
        if dis<50:
            standby=false
        time.sleep(0.3)
    
    incrementTen=Temperature/10 #Defines temperature in increments of 10
    incremenetOne=Temperature%10 #Defines temperature in increments of 1 (between 0 and 9)
    
    #Beeps the active buzzer
    for blips in range(0, incrementTen):
        beep(.1)
    for blips in range(0, incrementOne):
        beep(.1)
        
    loop()
        
def destory():
    Buzz.stop()					# Stop the passive buzzer
    GPIO.output(Buzzer, 1)		# Set passive Buzzer pin to High
    GPIO.output(BuzzerPin, GPIO.HIGH) #Set active buzzer pin to High
    GPIO.cleanup()				# Release resource

if __name__ == '__main__':		# Program start from here
    setup()
    try:
        loop()
    except KeyboardInterrupt:  	# When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destory()
