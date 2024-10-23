import RPi.GPIO as GPIO
import time

#Buzzers Setup
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

def stop():
    GPIO.output(activePin, GPIO.HIGH) #Set active buzzer pin to High