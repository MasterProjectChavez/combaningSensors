#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import ultrasonic_ranging as sonicSensor
import button
import thermistor as temperatureSensor
import passiveBuzzer
import activeBuzzer

#Ultrasonic sensor setup
sonicTrigPin=12 #Pin conflict
sonicEchoPin=11 #Pin conflict

#Buzzers Setup
activePin = 11 #Pin conflict
passivePin= 11 #Pin conflict

#Button1 setup
buttonPin = 11 #Pin conflict
buttonGPin   = 12 #Pin conflict
buttonRPin   = 13 #Pin conflict

#Button2 setup
button2Pin = 11 #Pin conflict
button2GPin   = 12 #Pin conflict
button2RPin   = 13 #Pin conflict

#Analog temperature sensor setup
temperaturePin = 17

Temperature=70 #Default temperature of sensor is 70 degrees Fahrenheit

CL = [0, 131, 147, 165, 175, 196, 211, 248]		# Frequency of Low C notes

CM = [0, 262, 294, 330, 350, 393, 441, 495]		# Frequency of Middle C notes

CH = [0, 525, 589, 661, 700, 786, 882, 990]		# Frequency of High C notes
song_1=[] #Initializes an array for frequencies of type integer
beat_1=[] #Initializes an array for beats of type integer

def loop(): #Normal behavior
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
    passiveBuzzer.stop() # Stop the passive buzzer
    activeBuzzer.stop()
    sonicSensor.destroy() #Cleanup
    button.destroy() #Cleanup
    GPIO.cleanup()				# Release resource

if __name__ == '__main__':		# Program start from here
    passiveBuzzer.setup(passivePin) #Sets up passive buzzer
    activeBuzzer.setup(activePin) #Sets up active buzzer
    sonicSensor.setup(sonicTrigPin, sonicEchoPin) #Sets up ultrasonic sensor
    button.setup(buttonPin, buttonGPin, buttonRPin) #Sets up increase temperature button
    button.setup(button2Pin, button2GPin,button2RPin) #Sets up decrease temperature button
    temperatureSensor.setup()
    try:
        loop()
    except KeyboardInterrupt:  	# When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destory()
