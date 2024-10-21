#!/usr/bin/env python3

import RPi.GPIO as GPIO
# or, for pin numbering(the small gray numbering on the board), choose BOARD 
GPIO.setmode(GPIO.BOARD)
# It only affects any ports you have set in the current program. It resets any ports you have used in this program back to input mode.
# should not be at the start of program
GPIO.cleanup()
import time

TRIG = 11
ECHO = 12
BuzzerPin = 13
# these are the pins on the sensor

def setup():
    GPIO.setmode(GPIO.BOARD)
    # Setup for ultrasonic sensor
    GPIO.setup(TRIG, GPIO.OUT) # set Trig as output
    GPIO.setup(ECHO, GPIO.IN) # set Echo as input

    # Setup for buzzer
    GPIO.setup(BuzzerPin, GPIO.OUT)
    GPIO.output(BuzzerPin, GPIO.HIGH) #Sets the output of the GPIO pin to high (3.3V) gpio lib does not appear to support 5V



def distance():
    GPIO.output(TRIG, 0) # sets the trigger pin to low (0V)
    time.sleep(0.000002) # pauses for said amount
    GPIO.output(TRIG, 1) # switch the port/pin to 3.3V (equals 1/GPIO.HIGH/True)
    time.sleep(0.00001)
    GPIO.output(TRIG, 0)
"""The condition is used to wait for the signal to change from low (0) to high (1). Once the signal is high, the code records the timestamp as pulse_end. 
The difference between the recorded timestamps is the duration of the pulse, which can be used to calculate the distance to an object"""
    while GPIO.input(ECHO) == 0: 
        a = 0
    time1 = time.time()
    while GPIO.input(ECHO) == 1:
        a = 1
    time2 = time.time()

    during = time2 - time1
    return during * 340 / 2 * 100

def buzzer_on():
    GPIO.output(BuzzerPin, GPIO.LOW)

def buzzer_off():
    GPIO.output(BuzzerPin, GPIO.HIGH)


def beep(duration):
    buzzer_on()
    time.sleep(duration)
    buzzer_off()
    time.sleep(duration)

def loop():
    while True:
        dis = distance()
        print(dis, 'cm')
 
# if the object is within 5 cm, buzz constantly
        if dis < 5: 
            buzzer_on()
# if the object is within 30 cm
        elif dis < 30:  
# decrease beep interval as object gets closer
            beep_interval = (dis - 5) / 50.0 
 # just an example scaling
            beep(beep_interval)
        else:
            buzzer_off()

        time.sleep(0.3)



def destroy():
    GPIO.cleanup()

if __name__ == "__main__":
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
