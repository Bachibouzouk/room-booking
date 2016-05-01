from django.db import models
from random import randint
from django.utils import timezone

from .date_play import convert_timeslot_to_date, TimeSlot



def random_date(start=timezone.datetime(1990,10,1,10,2,tzinfo=timezone.utc), end=timezone.now()):
    
    return start + timezone.timedelta(
        seconds=randint(0, int((end - start).total_seconds())))


class Classroom(models.Model):
    """a classroom has a name and a location plus a number of seats"""
    name = models.CharField(max_length = 200, unique = True)
    location = models.CharField(max_length = 200)
    number_seats = models.IntegerField(default = 1) 
        
    
    def __str__(self):
        return self.name
        
    def is_booked(self,date):
        """
            will return false if there is no conflict with existing bookings
            will return true otherwise
            any lists or nested list can be passed as an argument
            numpy would do a faster job...
        """
        
        if hasattr(date,'__iter__'):
            dates = date
            answers = []
            for date in dates:
                answers.append(self.is_booked(date))
            return answers
        
        if isinstance(date,TimeSlot):
            conflicts = self.booking_set.filter(date_start__lt=date.date_stop,date_stop__gt=date.date_start)
            if len(conflicts):
                return True
            else:
                return False
        elif isinstance(date,str):
            date_start,date_stop=convert_timeslot_to_date(date)
            conflicts = self.booking_set.filter(date_start__lt=date_stop,date_stop__gt=date_start)
            if len(conflicts):
                return True
            else:
                return False
        else:
            msg = """The method cannot take a %s type as an argument, the accepted types are %s and string
                  """%(type(date).__name__,TimeSlot.__name__)
            print(msg)
            raise TypeError(msg)

        
class Booking(models.Model):
    
    classroom= models.ForeignKey(Classroom, on_delete=models.CASCADE, null=True)
    date_start = models.DateTimeField(default=timezone.now)
    date_stop = models.DateTimeField(default=timezone.now)
    
    email = models.EmailField(default="abc@mail.mcgill.ca")
    
    max_booking = 4 #hours

    
    def __str__(self):
        return "%s to %s by %s"%(
        self.date_start.strftime("%Y-%m-%d from %H:%M"),
        self.date_stop.strftime("%H:%M"),
        self.email)

    def display(self):
        return self.__str__()
        
    def reminder(self):
        """this function should send a reminder to the person who booked the meeting"""        
        
    def cancel(self):
        """
        this function should send an email to the person who made the booking to to tell them it has been cancelled
        it should then delete the booking                
        """
        
class RandomUser(models.Model):
    
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE,null=True)
    email = models.EmailField()

    def __str__(self):
        return self.email
