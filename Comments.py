#!/usr/bin/env python3

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.cleanup()
import time

TRIG = 11
ECHO = 12
BuzzerPin = 13

def setup():
    GPIO.setmode(GPIO.BOARD)
    # Setup for ultrasonic sensor
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    
    # Setup for buzzer
    GPIO.setup(BuzzerPin, GPIO.OUT)
    GPIO.output(BuzzerPin, GPIO.HIGH)



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
