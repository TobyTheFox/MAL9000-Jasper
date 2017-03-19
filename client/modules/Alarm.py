import time
import multiprocessing
import Calendar
import re
import datetime

class Alarm_Clock:
        alarm_time = None #In UTC time form like 1489890471.866293
        alarm_set = False
        p = None

        def __init__(self):
                return

        def checkTime(self):
                '''If alarm time - current time is less than 0 sound the alarm!'''
                while(True):
                        if self.alarm_time - time.time() <= 0:
                                print "THE ALRAM IS GOING OFF"
                                for i in range(1):
                                        print "BEEP"
                                return(True)
                        else:
                                #print(self.alarm_time-time.time())
                                time.sleep(20)

        def set_alarm(self, profile, mic):
                wake_up_dt = datetime.datetime.strptime(Calendar.timeWakeUp(profile, mic), "%Y-%m-%dT%H:%M:%SZ")
                self.alarm_time = time.mktime(wake_up_dt.timetuple())
                mic.say("I have set your alarm") 
                return
 
        def start(self, profile, mic):
                '''Starts thread that checks if alarm is to go off or not'''
                if self.alarm_set:
                         self.stop()

                self.alarm_set = True       
                self.p = multiprocessing.Process(target=self.checkTime)

                self.p.start()
                return

        def stop(self, profile, mic):
                '''Cancels the alarm'''
                if self.alarm_set:
                        self.p.terminate()
                        self.alarm_set = False
                        mic.say("I have stopped your alarm, Toby")
                else:
                        mic.say("I'm sorry, Toby. I'm afraid I can't do that. You have no alarm to stop.")
                return

WORDS = ["Alarm"]

alarm = None

def handle(text, mic, profile):
        global alarm
        if bool(re.search('Set', text, re.IGNORECASE)):
                alarm = Alarm_Clock()
                alarm.set_alarm(profile, mic)
                alarm.start(profile, mic)
        
        if bool(re.search('Stop', text, re.IGNORECASE)):
                try:
                        alarm.stop(profile, mic)
                except:
                        mic.say("I'm sorry, Toby. I'm afraid I can't do that. You have no alarm to stop.")
def isValid(text):
    return bool(re.search(r'alarm', text, re.IGNORECASE))
