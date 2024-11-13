#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time as t
import button
import temp as temperatureSensor
import tempspeaker 

#Button1 setup
buttonPin = 11
buttonGPin   = "3V3" #Assigned to voltage pin
buttonRPin   = "GND" #Assigned to default

#Button2 setup
button2Pin = 12
button2GPin   = "3V3" #Assigned to voltage pin
button2RPin   = "GND" #Assigned to default

#Digital temperature sensor setup
#N/A

#Output
outputPin=33


setTemperature=70 #Default temperature of sensor is 70 degrees Fahrenheit


def loop(): #Normal behavior
    measuredTemperature=temperatureSensor.read() 
    fahrenheit = (measuredTemperature * 1.8) + 32
    fahrenheit = int(fahrenheit)
    output = f"{fahrenheit} degrees"
    setTemperature =  fahrenheit
    tempspeaker.speak(output)
    
    
    """
    if(measuredTemperature<setTemperature):
        GPIO.output(outputPin, GPIO.HIGH)
    elif(measuredTemperature>setTemperature):
        GPIO.output(outputPin, GPIO.LOW)
     """   
        
def destory():		
    button.destroy() #Cleanup
    GPIO.cleanup()				# Release resource

if __name__ == '__main__':		# Program start from here
    GPIO.setmode(GPIO.BOARD)		# Numbers GPIOs by physical location
    button.setup(buttonPin, 0)
    button.setup(button2Pin, 1)
    temperatureSensor.setup()
    try:
        loop()
    except KeyboardInterrupt:  	# When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destory()
