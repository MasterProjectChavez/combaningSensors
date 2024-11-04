#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import ultrasonic_ranging as sonicSensor
import button
import thermistor as temperatureSensor
import passiveBuzzer
import activeBuzzer

#Ultrasonic sensor setup
sonicTrigPin=11
sonicEchoPin=22  

#Buzzers Setup
activePin = 13
passivePin= 29

#Button1 setup
buttonPin = 37
#buttonGPin   = "3V3" #Assigned to voltage pin
#buttonRPin   = "GND" #Assigned to default

#Button2 setup
button2Pin = 15
#button2GPin   = "3V3" #Assigned to voltage pin
#button2RPin   = "GND" #Assigned to default

#Analog temperature sensor setup
temperaturePin = 33

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
        passiveBuzzer.Buzz.ChangeFrequency(song_1[i])	# Change the frequency along the song note
        time.sleep(beat_1[i] * 0.5)		# delay a note for beat * 0.5s
        
    #Resets song_1 and beat_1 for the next iteration
    song_1=[]
    beat_1=[]

    for time in range(0, 20): #Waits for input from buzzer for 20 seconds.
        time.sleep(1)
        
        
    
    loop() #Return to ultrasonic sensor
        
def destory():		
    passiveBuzzer.stop() # Stop the passive buzzer
    activeBuzzer.stop()
    sonicSensor.destroy() #Cleanup
    button.destroy() #Cleanup
    GPIO.cleanup()				# Release resource

### button.py
import RPi.GPIO as GPIO
import combined
import activeBuzzer

BtnPin = 11
Gpin   = 12
Rpin   = 13
type=-1

def setupButton(buttonPin, localGpin, localRpin, thisType):
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


###activeBuzzer.py
import RPi.GPIO as GPIO
import time

#activeBuzzer Setup
activePin = 11 #Pin conflict

def setup(thisPin):#Sets up Active buzzer
    global BuzzerPin
    BuzzerPin = thisPin
    #GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
    GPIO.setup(thisPin, GPIO.OUT)
    GPIO.output(thisPin, GPIO.HIGH)
    
def on(): #Turns Active Buzzer on
    GPIO.output(BuzzerPin, GPIO.LOW)

def off(): #Turns Active Buzzer off
    GPIO.output(BuzzerPin, GPIO.HIGH)
    
def beep(x): #Prompts the active buzzer to beep
    on()
    time.sleep(x)
    off()
    time.sleep(x)

###passiveBuzzer.py

import RPi.GPIO as GPIO
import time

thisPin=11 #Override with input from setup

def setup(passivePin): # Sets up Passive buzzer
    thisPin=passivePin
    #GPIO.setmode(GPIO.BOARD)		# Numbers GPIOs by physical location
    GPIO.setup(passivePin, GPIO.OUT)	# Set pins' mode is output
    global Buzz						# Assign a global variable to replace GPIO.PWM 
    Buzz = GPIO.PWM(passivePin, 440)	# 440 is initial frequency.
    Buzz.start(50)					# Start Buzzer pin with 50% duty ration

def stop():
    Buzz.stop()
    GPIO.output(thisPin, 1)		# Set passive Buzzer pin to High

def stop():
    GPIO.output(activePin, GPIO.HIGH) #Set active buzzer pin to High

###thermistor.py
#!/usr/bin/env python3
import PCF8591 as ADC
import RPi.GPIO as GPIO
import time
import math

DO = 17
#GPIO.setmode(GPIO.BCM)

def setup(sensorInput):
	DO=sensorInput
	ADC.setup(0x48)
	GPIO.setup(DO, GPIO.IN)

def Print(x):
	if x == 1:
		print ('')
		print ('***********')
		print ('* Better~ *')
		print ('***********')
		print ('')
	if x == 0:
		print ('')
		print ('************')
		print ('* Too Hot! *')
		print ('************')
		print ('')

def loop():
	status = 1
	tmp = 1
	while True:
		analogVal = ADC.read(0)
		Vr = 5 * float(analogVal) / 255
		Rt = 10000 * Vr / (5 - Vr)
		temp = 1/(((math.log(Rt / 10000)) / 3950) + (1 / (273.15+25)))
		temp = temp - 273.15
		print ('temperature = ', temp, 'C')

		# For a threshold, uncomment one of the code for
		# which module you use. DONOT UNCOMMENT BOTH!
		#################################################
		# 1. For Analog Temperature module(with DO)
		tmp = GPIO.input(DO)
		# 
		# 2. For Thermister module(with sig pin)
		#if temp > 33:
		#	tmp = 0
		#elif temp < 31:
		#	tmp = 1
		#################################################

		if tmp != status:
			Print(tmp)
			status = tmp

		time.sleep(0.2)

if __name__ == '__main__':
	try:
		setup()
		loop()
	except KeyboardInterrupt: 
		pass	

###ultrasonic_ranging.py
#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time

TRIG = 11
ECHO = 12

def setup(trigPin, echoPin):
	TRIG=trigPin
	ECHO=echoPin
	#GPIO.setmode(GPIO.BOARD)
	GPIO.setup(TRIG, GPIO.OUT)
	GPIO.setup(ECHO, GPIO.IN)

def distance():
	GPIO.output(TRIG, 0)
	time.sleep(0.000002)

	GPIO.output(TRIG, 1)
	time.sleep(0.00001)
	GPIO.output(TRIG, 0)

	
	while GPIO.input(ECHO) == 0:
		a = 0
	time1 = time.time()
	while GPIO.input(ECHO) == 1:
		a = 1
	time2 = time.time()

	during = time2 - time1
	return during * 340 / 2 * 100

def loop():
	while True:
		dis = distance()
		print (dis, 'cm')
		print ('')
		time.sleep(0.3)

def destroy():
	GPIO.cleanup()

if __name__ == "__main__":
	setup()
	try:
		loop()
	except KeyboardInterrupt:
		destroy()


if __name__ == '__main__':		# Program start from here
    GPIO.setmode(GPIO.BOARD)		# Numbers GPIOs by physical location
    passiveBuzzer.setup(passivePin) #Sets up passive buzzer
    activeBuzzer.setup(activePin) #Sets up active buzzer
    sonicSensor.setup(sonicTrigPin, sonicEchoPin) #Sets up ultrasonic sensor
    button.setup(buttonPin, buttonGPin, buttonRPin, 0) #Sets up increase temperature button
    button.setup(button2Pin, button2GPin,button2RPin, 1) #Sets up decrease temperature button
    temperatureSensor.setup(temperaturePin)
    try:
        loop()
    except KeyboardInterrupt:  	# When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destory()
