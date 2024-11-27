#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import RPi.GPIO as GPIO
import time
import subprocess

# DS18B20 global variable
ds18b20 = ''

# GPIO pins for the buttons
BUTTON_UP_PIN = 17    # Button to increment set temperature
BUTTON_DOWN_PIN = 27  # Button to decrement set temperature

# Default set temperature
set_temperature = 71.6  # Default set temperature in Fahrenheit

# Timing constants
BUTTON_DEBOUNCE_TIME = 0.2  # Debounce time in seconds
TEMP_CHECK_INTERVAL = 1     # Temperature check interval in seconds

# Variables to track button state and timing
last_button_up_state = GPIO.HIGH
last_button_down_state = GPIO.HIGH
last_button_up_time = 0
last_button_down_time = 0

# Flag to prevent repeated announcements
temp_met_announced = False

# Setup function
def setup():
    global ds18b20

    # Setup GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_UP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BUTTON_DOWN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Find the DS18B20 sensor
    for i in os.listdir('/sys/bus/w1/devices'):
        if i.startswith('28-'):  # DS18B20 devices start with '28-'
            ds18b20 = i
            break
    else:
        raise RuntimeError("No DS18B20 sensor found!")

# Read temperature function
def read():
    location = f'/sys/bus/w1/devices/{ds18b20}/w1_slave'
    try:
        with open(location, 'r') as tfile:
            text = tfile.read()

        lines = text.strip().split("\n")
        if len(lines) < 2 or "YES" not in lines[0]:
            raise ValueError("Invalid sensor data")

        temperature_data = lines[1].split(" ")[9]
        temperature_celsius = float(temperature_data[2:]) / 1000
        temperature_fahrenheit = (temperature_celsius * 9 / 5) + 32
        return temperature_fahrenheit
    except Exception as e:
        print(f"Error reading temperature: {e}")
        return None

# Text-to-speech function using espeak (non-blocking)
def speak(message):
    # Use subprocess.Popen to run espeak without blocking
    subprocess.Popen(['espeak', message])

# Main loop function
def loop():
    global set_temperature, temp_met_announced
    global last_button_up_state, last_button_down_state
    global last_button_up_time, last_button_down_time

    print("Thermostat is running...")
    speak("Thermostat is ready.")

    last_temp_check_time = 0

    while True:
        current_time = time.time()

        # Check the UP button state
        button_up_state = GPIO.input(BUTTON_UP_PIN)
        if button_up_state != last_button_up_state:
            print(f"Button UP state changed to {'LOW' if button_up_state == GPIO.LOW else 'HIGH'}")
            last_button_up_state = button_up_state
            if button_up_state == GPIO.LOW:
                # Button pressed
                if current_time - last_button_up_time >= BUTTON_DEBOUNCE_TIME:
                    set_temperature += 1.0  # Increment by 1°F
                    print(f"Set temperature increased: {set_temperature:.1f}°F")
                    speak(f"The new set temperature is {set_temperature:.1f} degrees Fahrenheit.")
                    temp_met_announced = False  # Reset announcement flag
                    last_button_up_time = current_time

        # Check the DOWN button state
        button_down_state = GPIO.input(BUTTON_DOWN_PIN)
        if button_down_state != last_button_down_state:
            print(f"Button DOWN state changed to {'LOW' if button_down_state == GPIO.LOW else 'HIGH'}")
            last_button_down_state = button_down_state
            if button_down_state == GPIO.LOW:
                # Button pressed
                if current_time - last_button_down_time >= BUTTON_DEBOUNCE_TIME:
                    set_temperature -= 1.0  # Decrement by 1°F
                    print(f"Set temperature decreased: {set_temperature:.1f}°F")
                    speak(f"The new set temperature is {set_temperature:.1f} degrees Fahrenheit.")
                    temp_met_announced = False  # Reset announcement flag
                    last_button_down_time = current_time

        # Read current temperature every TEMP_CHECK_INTERVAL seconds
        if current_time - last_temp_check_time >= TEMP_CHECK_INTERVAL:
            current_temperature = read()
            if current_temperature is not None:
                print(f"Current temperature: {current_temperature:.1f}°F")
            else:
                print("Failed to read temperature")
            last_temp_check_time = current_time

            # Check if current temperature meets set temperature (within tolerance)
            tolerance = 0.5  # Degrees Fahrenheit
            if current_temperature is not None:
                if abs(current_temperature - set_temperature) <= tolerance and not temp_met_announced:
                    print("Current temperature meets the set temperature!")
                    speak(f"The current temperature of {current_temperature:.1f} degrees Fahrenheit meets the set temperature of {set_temperature:.1f} degrees Fahrenheit.")
                    temp_met_announced = True  # Set flag to prevent repeated announcements
                elif abs(current_temperature - set_temperature) > tolerance and temp_met_announced:
                    # Temperature has moved away from set point, reset announcement flag
                    temp_met_announced = False

        # Sleep for a short time to prevent high CPU usage
        time.sleep(0.05)  # Sleep for 50 milliseconds

# Destroy function to cleanup GPIO
def destroy():
    GPIO.cleanup()

# Main execution
if __name__ == '__main__':
    try:
        setup()
        loop()
    except KeyboardInterrupt:
        destroy()
    except RuntimeError as e:
        print(e)



