import time
import multiprocessing

class Alarm_Clock:
        alarm_time = None #In UTC time form like 1489890471.866293
        alarm_set = False
        p = None

        def __init__(self,alarm_time):
                self.alarm_time = alarm_time


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

        def start(self):
                '''Starts thread that checks if alarm is to go off or not'''
                print "STARTING ALARM for " + str(self.alarm_time)
                if self.alarm_set:
                         self.stop()

                self.alarm_set = True       
                self.p = multiprocessing.Process(target=self.checkTime)

                self.p.start()


        def stop(self):
                '''Cancels the alarm'''
                self.p.terminate()
                self.alarm_set = False 
