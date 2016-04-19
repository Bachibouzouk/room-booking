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
"""
this generates the dates from today and up to ndays in the future and their key is the weekday
0 for monday and so on
"""
import calendar


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
        
    
    