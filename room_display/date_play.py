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

timeslots=["%iam"%(i) for i in range(8,13)]+["%ipm"%(i) for i in range(1,10)]


def get_next_seven_days():
    today = timezone.now()
#    today = today.replace(tzinfo=timezone.pytz.utc)

    dates = [today + datetime.timedelta(days=i) for i in range(7)]
    weekdays=[weekday_names[datetime.datetime.weekday(date)] for date in dates]
   
    return dates,weekdays

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
#each new booking should have the time, so when we select the time wanted we can display all rooms which DO NOT clash
#print get_month_dates()
#for date in get_next_seven_days():
#    print date.isoformat()
    
    