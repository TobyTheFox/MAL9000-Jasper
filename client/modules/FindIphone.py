# -*- coding: utf-8 -*-
import re
from pyicloud import PyiCloudService
from pyicloud.exceptions import PyiCloudFailedLoginException

WORDS = ["FIND", "IPHONE", "PHONE", "RING"]

# SHOULD PROBABLY BE GLOBAL IN JASPER
AFFIRMATIVE = ["YES", "YEAH", "SURE", "YAH", "YA"]
NEGATIVE = ["NO", "NEGATIVE", "NAH", "NA", "NOPE"]

# iCloud Settings
ICLOUD_USERNAME = "toby@tobyfox.co.uk"
ICLOUD_PASSWORD = "Tobias00!"

def handle(text, mic, profile):
    """
        Makes your iPhone ring

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
    """
    try:
        api = PyiCloudService(ICLOUD_USERNAME, ICLOUD_PASSWORD)

        #----- 2 FACTOR
        if api.requires_2fa:
            mic.say("I'm sorry Toby, I need you to validate iCloud for me.")
            import click
            print "Two-factor authentication required. Your trusted devices are:"

            devices = api.trusted_devices
            for i, device in enumerate(devices):
                print "  %s: %s" % (i, device.get('deviceName',
                    "SMS to %s" % device.get('phoneNumber')))

            device = click.prompt('Which device would you like to use?', default=0)
            device = devices[device]
            api.send_verification_code(device)
            #if not api.send_verification_code(device):
            #    print "Failed to send verification code"
            #sys.exit(1)

            code = click.prompt('Please enter validation code')
            if not api.validate_verification_code(device, code):
                mic.say("Failed to verify verification code")
                sys.exit(1)

            #-------END 2 FACTOR


    except PyiCloudFailedLoginException:
        mic.say("Invalid Username & Password")
        return

    # All Devices
    devices = api.devices

    # Just the iPhones
    iphones = []

    # The one to ring
    phone_to_ring = None

    for device in devices:
        current = device.status()
        if "iPhone" in current['deviceDisplayName']:
            iphones.append(device)

    # No iphones
    if len(iphones) == 0:
        mic.say("No IPhones Found on your account")
        return

    # Many iphones
    elif len(iphones) > 1:
        #mic.say("There are multiple iphones on your account.")
        count = 0
        for phone in iphones:
            #WILL ALWAYS SELECT THE SECOND IPHONE AS THAT IS MINE
            count += 1
            if count != 2:
                continue #my iphone is second in list, so i removed the first
            #print(phone.status()['name'].replace(u"’","'"))
            #mic.say("Did you mean the {type} named {name}?".format(type=phone.status()['deviceDisplayName'], name=(phone.status()['name'].replace("’".decode('utf-8'),"'"))))
            #command = mic.activeListen()
            #if any(aff in command for aff in AFFIRMATIVE):
            phone_to_ring = phone
            break

    # Just one
    elif len(iphones) == 1:
        phone_to_ring = iphones[0]

    if not phone_to_ring:
        mic.say("You didn't select an iPhone")
        return

    phone_to_ring.play_sound()
    mic.say("Sending ring command to the phone now")

def isValid(text):
    """
        Returns True if input is related to the item.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return re.search(r'\bfind.*phone\b', text, re.IGNORECASE) or \
        re.search(r'\b(ring)?.*phone.*(ring)?\b', text, re.IGNORECASE)
