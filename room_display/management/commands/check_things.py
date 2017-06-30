from django.core.management.base import BaseCommand, CommandError

from django.utils import timezone

import datetime

from room_display.models import Classroom, Booking, random_date

from room_display.date_play import TimeSlot,get_next_seven_days, duration, duration_display

from room_display.registrar_output_converter import mainf

class Command(BaseCommand):

    def handle(self, *args, **options):
        # now do the things that you want with your models here
    
    
#        mainf()
#        ts=TimeSlot("2017-06-05 from 07:00 to 22:00",datestr=True)
#        
#        print(ts.date())        
#        cr = Classroom.objects.all()
#        print(duration)
#        print(duration_display)
#        good_cr =[]
#        for c in cr:
#            print(c.is_booked(ts))
#            if "Leacock132" in c.name:
##                c.make_hard_booking(ts)
#                print(c.booking_set.all())
##            print(c.is_booked(ts))
#            if c.is_booked(ts):
#                pass
#            else:
#                good_cr.append(c)
    
    
#            """
#            this allows to find all the bookings made per room by one email after a given date
#            """
#            print(c.booking_set.filter(email = "troll@test.caution",date_start__gt=ts.date_start))
        
        
#        
#        print(good_cr)
#        print("#"*15)
#        
#        
#        """
#        this allows to find all the bookings made by one email after a given date
#        
#        """
        a_user = "soft.test@mcgill.ca"        
        ts = TimeSlot("2018-06-05 from 07:00 to 22:00", datestr = True)
#        cr = Classroom.objects.get(name="Leacock132")
        cr2 = Classroom.objects.get(name="Boardroom")
        
#        cr.make_soft_booking(ts, a_user)
        
        cr2.make_soft_booking(ts, a_user)        
        
        
        
#        bk = Booking.objects.filter(email ="troll@test.caution",date_start__gt=ts.date_start)
#        print(bk)
#        'America/Montreal'

#        bk = Booking.objects.filter(date_start__lt=ts.date_stop,date_stop__gt=ts.date_start)
        
                
        
#        bad_cr = []
#        
#        for b in bk :
#            if not b.classroom in bad_cr:
#                bad_cr.append(b.classroom)
#        
#        print(bad_cr)
#        good_cr = Classroom.objects.filter(is_booked__ts == False)
    
        
    
    
#        cr=Classroom.objects.get(name="Leacock132")
#        
##        print(cr.booking_set.all())
#        ts=TimeSlot("2016-05-02 from 09:00 to 10:00",datestr=True)
##        "2016-05-02 from 10:00 to 10:30"
#        print(cr.is_booked(ts))
#        
#        ts=TimeSlot("2016-05-02 from 11:00 to 12:00",datestr=True)
#        
#        print(cr.booking_set.filter(date_start__lt=ts.date_stop,date_stop__gt=ts.date_start))
##        "2016-05-02 from 10:00 to 10:30"
#        print(cr.is_booked(ts))      
#        
##        print(cr.booking_set.all())
#        ts=TimeSlot("2016-05-02 from 09:00 to 09:59",datestr=True)
##        "2016-05-02 from 10:00 to 10:30"
#        print(cr.is_booked(ts))
#        
#        ts=TimeSlot("2016-05-02 from 11:01 to 12:00",datestr=True)
##        "2016-05-02 from 10:00 to 10:30"
#        print(cr.is_booked(ts))        
        
#        ts=TimeSlot("2016-05-02 from 10:00 to 13:30",datestr=True)
##        "2016-05-02 from 10:00 to 10:30"
#        a,b,c = get_next_seven_days()
#        print(cr.is_booked(c))        
        
#        bl=cr.booking_set.filter(date_start__lte=ts.date_stop,date_stop__gte=ts.date_start)
#        print(len(bl))
#        for b in bl:
#            print(b)
            
            
#        cr.save()
#        for i in range(3):
#            adate = random_date()
#            adate2 = adate + timezone.timedelta(hours=1)
#            cr.booking_set.create(date_start = adate, date_stop = adate2)
#        cr.save()
#        
#
#        cr=Classroom(name="Bell",location="Rutherford",number_seats=70)
#        cr.save()
#        users=["rte@epfl.ch","lapremiere@cbc.ca"]
#        
#        for user in users:
#            adate = random_date()
#            adate2 = adate + timezone.timedelta(hours=1)
#            cr.booking_set.create(date_start = adate, date_stop = adate2, email=user)
#        cr.save()        
#        
#        cr=Classroom(name="Boardroom",location="Rutherford",number_seats=60)
#        cr.save()
#        for i in range(3):
#            cr.booking_set.create()
#        
#        cr.save()          
#        
#        print(Classroom.objects.all())