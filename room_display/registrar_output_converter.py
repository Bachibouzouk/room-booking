# -*- coding: utf-8 -*-
"""
Created on Mon May 29 22:28:47 2017

@author: pfduc
"""

import csv
from django.utils import timezone

WEEKDAYS_CODE = ['M','T','W','R','F','S','U']

from room_display.date_play import HOUR_MIN, HOUR_MAX, TimeSlot

def mainf():
    fname = "C:\\Users\\pfduc\\Documents\\room-booking\\Output_by_mcgill_system.csv"
    
    start_data = False
    
    output_data = []
    
    with open(fname, 'r') as csvfile:
        
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    
        for row in spamreader:
            
            if "For Week" in row[0]:
                weekdate_start = row[0].replace("For Week",'').strip()
                
                weekdate_start = weekdate_start.split(' to ')[0]
                
                weekdate_start =  timezone.datetime.strptime(weekdate_start, '%d-%b-%Y')
            
            #parse only the meaningful data
            if start_data:

                weekdays = row[3].strip().split(' ')
 
                time_start, time_stop = row[4].strip().split('  -  ')
                
                #will contain which time slots aren't available so we can
                #hardbook them
                timeslots = []
                
                #loop over the weekdays
                for weekday in WEEKDAYS_CODE:
                    
                    if weekday in weekdays:
                    #the room is available on that day, so we keep track of the
                    #time at which it isn't in order to hardbook it
                    
                    #get the date of that day from the one of the beginning of 
                    #the week
                        cur_weekdate = weekdate_start + \
                        timezone.timedelta(days = WEEKDAYS_CODE.index(weekday),
                                               hours = HOUR_MIN)
                                           
                        #before the period the room is available we
                        #need to recreate a hard booking
                        hb_stop = timezone.datetime.strptime(
                        "%s %s"%(cur_weekdate.date(),time_start),
                        '%Y-%m-%d %H:%M')
                        
                        #compare the hour with the min allowed hour
                        if hb_stop.hour > HOUR_MIN:
                            
                            ts = TimeSlot("%s from %02d:00 to %s"%(
                                hb_stop.strftime("%Y-%m-%d"),
                                HOUR_MIN,
                                hb_stop.strftime("%H:%M")),
                            datestr = True)
                            
                            timeslots.append(ts)

                        
                        #after the period where the room is available we
                        #need to recreate a hard booking
                        hb_restart = timezone.datetime.strptime(
                        "%s %s"%(cur_weekdate.date(),time_stop),
                        '%Y-%m-%d %H:%M')
                        
                        #compare the hour with the max allowed hour
                        if hb_restart.hour < HOUR_MAX:
                            
                            ts = TimeSlot("%s to %02d:00"%(
                                hb_restart.strftime("%Y-%m-%d from %H:%M"),
                                HOUR_MAX),
                            datestr = True)
                            
                            timeslots.append(ts)
                    else:
                    #the room isn't available so we'll hardbook on whole day
                        cur_weekdate = weekdate_start + \
                        timezone.timedelta(days = WEEKDAYS_CODE.index(weekday),
                                           hours = HOUR_MIN)
                        
                        #create a timeslot for the whole day
                        ts = TimeSlot(cur_weekdate,
                                      duration = HOUR_MAX - HOUR_MIN)
                    
                        timeslots.append(ts)

                #the information needed to do the hard booking :
                #room name and timeslots
                booking = {
                "room" : "%s %s"%(row[1], row[2]),
                "timeslots" : timeslots      
                }
                
                output_data.append(booking)
                
            #from this row the data starts to be interesting to parse
            if "RDEF CODE" in row[0]:
                
                start_data = True

    return output_data