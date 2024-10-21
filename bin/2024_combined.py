#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import ultrasonic_ranging as sonicSensor
import button

#Ultrasonic sensor setup
sonicOutPin=11 #Pin conflict
sonicInPin=12 #Pin conflict

#Buzzers Setup
activePin = 11 #Pin conflict
passivePin= 11 #Pin conflict

#Button1 setup
buttonPin = 11 #Pin conflict
buttonGPin   = 12 #Pin conflict
buttonRPin   = 13

#Button2 setup
button2Pin = 11 #Pin conflict
button2GPin   = 12 #Pin conflict
button2RPin   = 13 #Pin conflict

Temperature=70 #Default temperature of sensor is 70 degrees Fahrenheit

CL = [0, 131, 147, 165, 175, 196, 211, 248]		# Frequency of Low C notes

CM = [0, 262, 294, 330, 350, 393, 441, 495]		# Frequency of Middle C notes

CH = [0, 525, 589, 661, 700, 786, 882, 990]		# Frequency of High C notes
song_1=[] #Initializes an array for frequencies of type integer
beat_1=[] #Initializes an array for beats of type integer
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

def setupPassive(passivePin): # Sets up Passive buzzer
    GPIO.setmode(GPIO.BOARD)		# Numbers GPIOs by physical location
    GPIO.setup(passivePin, GPIO.OUT)	# Set pins' mode is output
    global Buzz						# Assign a global variable to replace GPIO.PWM 
    Buzz = GPIO.PWM(passivePin, 440)	# 440 is initial frequency.
    Buzz.start(50)					# Start Buzzer pin with 50% duty ration
      
def setupActive(activePin):#Sets up Active buzzer
    global BuzzerPin
    BuzzerPin = activePin
    GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
    GPIO.setup(activePin, GPIO.OUT)
    GPIO.output(activePin, GPIO.HIGH)
    
def on(): #Turns Active Buzzer on
    GPIO.output(BuzzerPin, GPIO.LOW)

def off(): #Turns Active Buzzer off
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
    standby=True
    while standby: #Keeps the ultrasonic sensor on standby when nobody is within 50 cm of the thermostat
        dis = sonicSensor.distance() #Stores the value from ultrasonic sensor
        print (dis, 'cm') # Prints to console
        print ('')
        if dis<50: #If someone is detected within 50 cm (half a meter), then the thernometer will beep
            standby=False #Breaks our of the while loop to proceed
        time.sleep(1)  


    
    incrementTen=Temperature/10 #Defines temperature in increments of 10
    incremenetOne=Temperature%10 #Defines temperature in increments of 1 (between 0 and 9)
    
    #Define the passive buzzer's rhythm based on temperature
    """ We may not need to use the active buzzer because the passive buzzer contains multiple frequencies
    that can be used to differentiate each increment
    for blips in range(0, incrementTen):
        beep(.1)
    for blips in range(0, incrementOne):
        beep(.1)
    """
    
    #Writes instructions for the passive buzzer
    for incrementTen in range(0, incrementTen):
        song_1.append(CH[1])
        beat_1.append(1)

    for incrementOne in range(0, incrementOne):
        song_1.append(CL[1])
        beat_1.append(2)

    #Executes instructions to the passive buzzer
    for i in range(1, len(song_1)):		# Play song 1 (executes the previously written instructions)
        Buzz.ChangeFrequency(song_1[i])	# Change the frequency along the song note
        time.sleep(beat_1[i] * 0.5)		# delay a note for beat * 0.5s
        
    #Resets song_1 and beat_1 for the next iteration
    song_1=[]
    beat_1=[]

    for time in range(0, 100): #Checks for input changes. Limitation: cannot change temperature 
        #while reading temperature 
        button.detect()
        if True:
            Temperature+=1
        elif True:
            Temperature-=1
    
    loop()
        
def destory():
    Buzz.stop()					# Stop the passive buzzer
    GPIO.output(passivePin, 1)		# Set passive Buzzer pin to High
    GPIO.output(activePin, GPIO.HIGH) #Set active buzzer pin to High
    sonicSensor.destroy() #Cleanup
    button.destroy() #Cleanup
    GPIO.cleanup()				# Release resource

if __name__ == '__main__':		# Program start from here
    setupPassive(passivePin) #Sets up passive buzzer
    setupActive(activePin) #Sets up active buzzer
    sonicSensor.setup(sonicOutPin, sonicInPin) #Sets up ultrasonic sensor
    button.setup(buttonPin, buttonGPin, buttonRPin) #Sets up increase temperature button
    button.setup(button2Pin, button2GPin,button2RPin) #Sets up decrease temperature button
    try:
        loop()
    except KeyboardInterrupt:  	# When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destory()
