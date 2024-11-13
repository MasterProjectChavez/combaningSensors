import subprocess
import time 
#import speech_recognition as sr

def speak(text):
	text = text.replace(" ", "_")
	subprocess.run((
		"espeak \"" + 
		text +
		" 2>/dev/null"
		).split(" ")
	) 

if __name__ == '__main__':
	speak("the Temperature is 70 degrees")
