import RPi.GPIO as GPIO
import os
#Script that runs on startup to run MAL if the on button is pressed on pin 3 to ground

def startMAL():
    '''When on button pressed, MAL starts'''
    os.system('python jasper.py')
    GPIO.remove_event_detect(3)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(3, GPIO.BOTH, callback=startMAL, bouncetime=300)

