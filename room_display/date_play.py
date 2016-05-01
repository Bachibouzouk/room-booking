# -*- coding: utf-8 -*-
"""
Created on Sat Apr 16 23:16:18 2016

@author: pfduc
"""

#from datetime import date
#from dateutil.relativedelta import relativedelta
#
#
#mydates=[]
#
#for i in range(60):
#
#    mydates.append(date.today() + absolutedelta(day=+i))
#    
#    print(mydates[i]).isoformat()
#
import numpy as np
import datetime
from django.utils import timezone
"""
this generates the dates from today and up to ndays in the future and their key is the weekday
0 for monday and so on
"""
import calendar

weekday_names=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
#u = datetime.utcnow()
#u = u.replace(tzinfo=pytz

booking_step=1 #unit hour

timeslots=range(8,22,booking_step)


class TimeSlot():
    
    date_start = None
    duration = None
    date_stop = None
    has_booking = False
    
    def __init__(self,date,hour=None,duration = booking_step,datestr=False):
        """create a TimeSlot with a start date and a duration"""
        if datestr:
           
            self.date_start,self.date_stop = convert_timeslot_to_date(date)
            self.duration = (self.date_stop - self.date_start).total_seconds()/3600.
            
        else:
            
            if hour == None:
                self.date_start = date
            else:
                self.date_start = timezone.datetime.combine(date,datetime.time(hour))

                 
            
            self.duration = duration

            self.date_stop = self.date_start + timezone.timedelta(hours=self.duration)
        
        #make sure the date is not naive
        self.date_start = self.date_start.replace(tzinfo=timezone.utc) 
        #make sure the date is not naive
        self.date_stop = self.date_stop.replace(tzinfo=timezone.utc) 
        
    def __add__(self, TS_instance):
        """add two time slots together provided they are concommitent"""
        if isinstance(TS_instance,self.__class__):
            if TS_instance.date_start.strftime("%Y-%m-%d %H:%M") == self.date_stop.strftime("%Y-%m-%d %H:%M"):
                duration = self.duration + TS_instance.duration
                return TimeSlot(self.date_start, duration = duration)
            else:
                msg = """Your two instances of %s start and end time are not concommittent\nInstance 1 : %s\nInstance 2 : %s"""%(self.__class__.__name__,self,TS_instance)
                raise(ValueError,msg)
                
        elif isinstance(TS_instance,int):
            duration = self.duration + TS_instance
            return TimeSlot(self.date_start, duration = duration)
        else:
            msg = """You are trying to add a %s instance with a wrong type\n
                     Instance 1 : %s\nInstance 2 : %s
                  """%(self.__class__.__name__,self,TS_instance)
  
            raise(TypeError,msg)
    def __str__(self):
        """print the object"""
        return "%s to %s"%(
        self.date_start.strftime("%Y-%m-%d from %H:%M"),
        self.date_stop.strftime("%H:%M"))
    
    def hour(self):
        return "%s"%(self.date_start.strftime("%H:%M"))
    def date(self):
        return "%s"%(self.date_start.strftime("%Y-%m-%d"))
    
def convert_timeslot_to_date(datestr):
            date,duration_stop=datestr.split(' to')
            date,duration_start=date.split(' from')

            timefmt="%Y-%m-%d %H:%M"
           
            date_start = timezone.datetime.strptime(date+duration_start,timefmt).replace(tzinfo=timezone.utc)
            date_stop = timezone.datetime.strptime(date+duration_stop,timefmt).replace(tzinfo=timezone.utc)
            
            return date_start,date_stop

def append_timeslot(timeslot_list,datestr=True):
    
    appended_ts_list = []
    start = TimeSlot(timeslot_list.pop(0),datestr=datestr)
#    stop = start
    while not len(timeslot_list) == 0:
        cont = TimeSlot(timeslot_list.pop(0),datestr=datestr)
#        print(cont)
        try:
#            print "I am here"
            start = start + cont
#            print start
        except:        
            appended_ts_list.append(start)
#            print("sequence %i to %i"%(start, stop))
            start = cont
#            stop = start
    
    appended_ts_list.append(start)

    return appended_ts_list
#    print("sequence %i to %i"%(start, stop))
    
    
    
def get_next_seven_days():
    today = timezone.now()
#    today = datetime.datetime.now()
#    today = today.replace(tzinfo=timezone.pytz.utc)
#    datetime.datetime.date()11
    dates = [(today + datetime.timedelta(days=i)).date() for i in range(7)]
    weekdays=[weekday_names[datetime.datetime.weekday(date)] for date in dates]
   
    time_list=[]   
    for t in timeslots:
    
        date_list=[]
        for date in dates :
            ts=TimeSlot(date,hour=t)
#            print ts
            date_list.append(ts)
        time_list.append(date_list)
            
   
    return dates,weekdays,time_list

def get_month_dates(cur_month = datetime.date.today().month):
    myc = calendar.Calendar()

    dg = np.array([i for i in myc.itermonthdates(2016,cur_month)])

#myc=calendar.TextCalendar()
#
#print myc.formatmonth(2016,6)

    nweeks = 4
#store the dates in a scheduler
    ws = np.reshape(dg,(nweeks+1,7))
    return ws
    
#get_next_seven_days()
#each new booking should have the time, so when we select the time wanted we can display all rooms which DO NOT clash
#print get_month_dates()
#for date in get_next_seven_days()[0]:
#    for t in timeslots:
#        
#        d=timezone.datetime.combine(date,datetime.time(t))
#        d.replace(tzinfo=timezone.pytz.utc)
#        print d.isoformat()
#if __name__=="__main__":

booked_date=['2016-05-01 from 18:00 to 19:00', '2016-05-01 from 11:00 to 14:00', '2016-05-02 from 20:00 to 22:00']


#    ts_list = ['2016-05-01 from 08:00 to 09:00', '2016-05-01 from 09:00 to 10:00', '2016-05-02 from 10:00 to 11:00', '2016-05-02 from 11:00 to 12:00']
##
#    append_timeslot(ts_list)    
#    1+None
#    e=[1,2,3,6,7,8,10,11]
#    start=e.pop(0)
#    stop=start
#    while not len(e) == 0:
#        cont=e.pop(0)
#        if cont-stop == 1:
#            stop=cont
#        else:        
#            print("sequence %i to %i"%(start,stop))
#            start=cont
#            stop=start
#    print("sequence %i to %i"%(start,stop))
#    ts1=TimeSlot("2016-05-01 from 09:00 to 10:00",datestr=True)
##    date="21:07"
##    print ts1.date_start
##    
##    timefmt="%H:%M"
##    #print datetime.time.strptime(date,timefmt).
#    #adate = datetime.datetime.fromtimestamp("2016-04-30 19:59:27.598494")
#    ts2=TimeSlot("2016-05-01 from 10:00 to 11:00",datestr=True)
#    print ts1
#    print ts2
#    ts1 = ts1 + ts2
#    print ts1
