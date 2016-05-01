from django.core.management.base import BaseCommand, CommandError

from django.utils import timezone

from room_display.models import Classroom, Booking, random_date

from room_display.date_play import TimeSlot,get_next_seven_days

class Command(BaseCommand):

    def handle(self, *args, **options):
        # now do the things that you want with your models here
        cr=Classroom.objects.get(name="Leacock132")
        
#        print(cr.booking_set.all())
        ts=TimeSlot("2016-05-02 from 09:00 to 10:00",datestr=True)
#        "2016-05-02 from 10:00 to 10:30"
        print(cr.is_booked(ts))
        
        ts=TimeSlot("2016-05-02 from 11:00 to 12:00",datestr=True)
        
        print(cr.booking_set.filter(date_start__lt=ts.date_stop,date_stop__gt=ts.date_start))
#        "2016-05-02 from 10:00 to 10:30"
        print(cr.is_booked(ts))      
        
#        print(cr.booking_set.all())
        ts=TimeSlot("2016-05-02 from 09:00 to 09:59",datestr=True)
#        "2016-05-02 from 10:00 to 10:30"
        print(cr.is_booked(ts))
        
        ts=TimeSlot("2016-05-02 from 11:01 to 12:00",datestr=True)
#        "2016-05-02 from 10:00 to 10:30"
        print(cr.is_booked(ts))        
        
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