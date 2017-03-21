# -*- coding: utf-8-*-
import logging
from notifier import Notifier
from brain import Brain
import RPi.GPIO as GPIO
import sys
import os

class Conversation(object):
    def reset_pressed(self, input_pin):
        self.mic.say("Toby, I'm scared.")
        os.execl(sys.executable, sys.executable, *sys.argv)

    def __init__(self, persona, mic, profile):
        self._logger = logging.getLogger(__name__)
        self.persona = persona
        self.mic = mic
        self.profile = profile
        self.brain = Brain(mic, profile)
        self.notifier = Notifier(profile)
        
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(5, GPIO.BOTH, callback=self.reset_pressed)

    def handleForever(self):
        """
        Delegates user input to the handling function when activated.
        """
        self._logger.info("Starting to handle conversation with keyword '%s'.",
                          self.persona)
        while True:
            # Print notifications until empty
            notifications = self.notifier.getAllNotifications()
            for notif in notifications:
                self._logger.info("Received notification: '%s'", str(notif))

            self._logger.debug("Started listening for keyword '%s'",
                               self.persona)
            threshold, transcribed = self.mic.passiveListen(self.persona)
            self._logger.debug("Stopped listening for keyword '%s'",
                               self.persona)

            if not transcribed or not threshold:
                self._logger.info("Nothing has been said or transcribed.")
                continue
            self._logger.info("Keyword '%s' has been said!", self.persona)

            self._logger.debug("Started to listen actively with threshold: %r",
                               threshold)
            input = self.mic.activeListenToAllOptions(threshold)
            self._logger.debug("Stopped to listen actively with threshold: %r",
                               threshold)

            if input:
                self.brain.query(input)
            else:
                self.mic.say("Pardon?")
