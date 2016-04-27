from django.core.management.base import BaseCommand, CommandError

from django.utils import timezone

from room_display.models import Classroom, Booking, random_date

class Command(BaseCommand):

    def handle(self, *args, **options):
        # now do the things that you want with your models here
        cr=Classroom(name="Leacock132",location="Leacock",number_seats=700)
        cr.save()
        for i in range(3):
            adate = random_date()
            adate2 = adate + timezone.timedelta(hours=1)
            cr.booking_set.create(date_start = adate, date_stop = adate2)
        cr.save()
        

        cr=Classroom(name="Bell",location="Rutherford",number_seats=70)
        cr.save()
        users=["rte@epfl.ch","lapremiere@cbc.ca"]
        
        for user in users:
            adate = random_date()
            adate2 = adate + timezone.timedelta(hours=1)
            cr.booking_set.create(date_start = adate, date_stop = adate2, email=user)
        cr.save()        
        
        cr=Classroom(name="Boardroom",location="Rutherford",number_seats=60)
        cr.save()
        for i in range(3):
            cr.booking_set.create()
        
        cr.save()          
        
        print(Classroom.objects.all())