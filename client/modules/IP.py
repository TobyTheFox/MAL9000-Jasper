import re
import os
import random

WORDS = ["Address","IP"]

def isValid(text):
	return bool(re.search(r'\bIP\b', text, re.IGNORECASE)) or bool(re.search(r'\Address\b', text, re.IGNORECASE))

def getIP():
        ip_addr = str(os.popen('ifconfig wlan0 | grep "inet\ addr" | cut -d: -f2 | cut -d" " -f1').read())
        print(ip_addr)
        return ip_addr

def getIntro():
        intros = ["OK, you can find me at ", "My I P is ", "I'm at"]
        return random.choice(intros)

def handle(text, mic, profile):
        try:
                #gets IP and converts . to "dot" so he pronounces it, and adds a space after each character
                mic.say(getIntro() + (" ").join(getIP()).replace(".","dot"))

        except Exception as e:
                 print(e)
                 mic.say("I could not find my I P, sorry.")
