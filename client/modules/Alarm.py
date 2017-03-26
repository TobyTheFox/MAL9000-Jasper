import time
import multiprocessing
import Calendar
import re
import datetime
import os

class Alarm_Clock:
        alarm_time = None #In UTC time form like 1489890471.866293
        alarm_set = False
        alarm_going_off = False
        p = None

        def __init__(self):
                return

        def alarm_go_off(self, station_id):
                self.alarm_going_off = True
                os.system("pyradio --play "+str(station_id))
                return

        def checkTime(self):
                '''If alarm time - current time is less than 0 sound the alarm!'''
                while(True):
                        if self.alarm_time - time.time() <= 0:
                                self.alarm_go_off(15) #station id
                                return(True)
                        else:
                                time.sleep(20)

        def set_alarm(self, profile, mic):
                try:
                        #TODO: Change to start 1 hour before the event
                        wake_up_time = Calendar.timeWakeUp(profile, mic)
                        wake_up_dt = datetime.datetime.strptime(wake_up_time, "%Y-%m-%dT%H:%M:%SZ")
                        self.alarm_time = time.mktime(wake_up_dt.timetuple())
                        mic.say("I have set your alarm") 
                        return
                except:
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
                        os.system("pkill mplayer")
                        os.system("pkill pyradio")
                        if self.alarm_going_off:
                                self.alarm_going_off = False
                        else:
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
