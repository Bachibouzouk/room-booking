from django.db import models
from django import forms
from random import randint
from django.utils import timezone

from .date_play import convert_timeslot_to_date, TimeSlot, DATE_CHOICES, \
                        HOUR_CHOICES, HOUR_STOP_CHOICES, HOUR_MIN, booking_step#MINUTE_CHOICES
                        
                        
from .email_management import send_email, is_from_mcgill
import random
                        
                        
LOG_FILE_NAME = "soft_bookings.log"

BOOKING_FREE_TYPE = 0

BOOKING_SOFT_TYPE = 1

BOOKING_HARD_TYPE = 2

DEBUG = True

def random_date(start=timezone.datetime(1990, 10, 1, 10, 2, tzinfo=timezone.utc), end=timezone.now()):

    return start + timezone.timedelta(
        seconds=randint(0, int((end - start).total_seconds())))



class SelectDateTime(forms.Form):
    date = forms.ChoiceField(choices = DATE_CHOICES)#forms.DateField(widget = forms.SelectDateWidget(years=("2016","2017")))
#    delivery_time = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))
    timestart = forms.ChoiceField(choices = HOUR_CHOICES)
    
    timestop = forms.ChoiceField(choices = HOUR_STOP_CHOICES)    
    
    idn = forms.HiddenInput()
    
#    def __init__(self,*args,**kwargs):
#        print("inside constructor")
#        print("args")
#        print(args)
#        print("kwargs")
#        print(kwargs)
#        super(SelectDateTime,self).__init__(*args,**kwargs)
#        self.base_fields['timestop'].inital = 9.5
##        import ipdb;ipdb.set_trace()
##        print(self.timestart.initial)

#        self.initial['timestart'] = tstart
#    minute = forms.ChoiceField(choices = MINUTE_CHOICES)

class Calendar(forms.Form):

    date = forms.DateField(widget = forms.SelectDateWidget(years=("2016","2017")))
    
    
#class DateSelectorWidget(forms.widgets.MultiWidget):
#    def __init__(self, attrs=None):
#        # create choices for days, months, years
#        # example below, the rest snipped for brevity.
#        years = [(year, year) for year in (2011, 2012, 2013)]
#        _widgets = (
#            forms.widgets.Select(attrs=attrs, choices=days),
#            forms.widgets.Select(attrs=attrs, choices=months),
#            forms.widgets.Select(attrs=attrs, choices=years),
#        )
#        super(DateSelectorWidget, self).__init__(_widgets, attrs)
#
#    def decompress(self, value):
#        if value:
#            return [value.day, value.month, value.year]
#        return [None, None, None]
#
#    def format_output(self, rendered_widgets):
#        return ''.join(rendered_widgets)
#
#    def value_from_datadict(self, data, files, name):
#        datelist = [
#            widget.value_from_datadict(data, files, name + '_%s' % i)
#            for i, widget in enumerate(self.widgets)]
#        try:
#            D = timezone.datetime.date(
#                day=int(datelist[0]),
#                month=int(datelist[1]),
#                year=int(datelist[2]),
#            )
#        except ValueError:
#            return ''
#        else:
#            return str(D)

class Classroom(models.Model):
    """a classroom has a name and a location plus a number of seats"""
    name = models.CharField(max_length=200, unique=True)
    location = models.CharField(max_length=200)
    number_seats = models.IntegerField(default=1)

    def __str__(self):
        return self.name

    def is_booked(self, date):
        """
            will return false if there is no conflict with existing bookings
            will return true otherwise
            any lists or nested list can be passed as an argument
            numpy would do a faster job...
        """

        if hasattr(date, '__iter__'):
            dates = date
            answers = []
            for date in dates:
                answers.append(self.is_booked(date))
            return answers

        if isinstance(date, TimeSlot):
            conflicts = self.booking_set.filter(
                date_start__lt=date.date_stop, date_stop__gt=date.date_start)
                
            if len(conflicts) == 1:
#                print(conflicts)
                return conflicts[0].booking_type
                
            elif len(conflicts) > 1:
#                print(conflicts)
                msg = "There shouldn't be more than one existing booking"
                print(msg)
#                raise IndexError(msg)
                
            else:
                return BOOKING_FREE_TYPE
                
        elif isinstance(date, str):
            date_start, date_stop = convert_timeslot_to_date(date)
            conflicts = self.booking_set.filter(
                date_start__lt=date_stop, date_stop__gt=date_start)
                
            if len(conflicts) == 1:
#                print(conflicts)
                return conflicts[0].booking_type
                
            elif len(conflicts) > 1:
#                print(conflicts)
                msg = "There shouldn't be more than one existing booking"
                print(msg)
#                raise IndexError(msg)
                
            else:
                return BOOKING_FREE_TYPE
        else:
            msg = """The method cannot take a %s type as an argument, the accepted types are %s and string
                  """ % (type(date).__name__, TimeSlot.__name__)
            print(msg)
            raise TypeError(msg)
    
    def make_soft_booking(self, booking_timeslot, email):
        """
        this method recieve a timeslot and an email and creates a booking if it
        doesn't clash with an existing one
        """
        
        if isinstance(booking_timeslot, TimeSlot):
            #check that the email is from McGill 
            if is_from_mcgill(email):
                #check that the room isn't already booked
                if not self.is_booked(booking_timeslot):
                    self.booking_set.create(
                                        date_start=booking_timeslot.date_start,
                                        date_stop=booking_timeslot.date_stop,
                                        email=email,booking_type = BOOKING_SOFT_TYPE)
                    
                    #keep a record of the soft booking made
                    of = open(LOG_FILE_NAME,'a')
                    of.write("%s,\t"%(timezone.now()))
                    of.write("%s,\t"%(self.name))
                    of.write("%s,\t"%(booking_timeslot))
                    of.write("%s,\t"%(email))
                    of.write("SOFT booking,\n")
                    of.close()
                    return 0
                    
                else:
                    return 1
                    
            else:
                #the email isn't from McGill
                print("The email %s isn't from McGill, you can't use that service sorry")
                return 2
        else:
            raise TypeError("the timeslot instance is not of the right type")
    
    def make_hard_booking(self, booking_timeslot):
        """
        this method recieve a timeslot and an email and creates a booking if it
        doesn't clash with an existing one
        """
        
        if isinstance(booking_timeslot, TimeSlot):
            
            #check that the room isn't already booked
            cur_booking_type = self.is_booked(booking_timeslot)
            proceed_to_booking = True
            
            if cur_booking_type == BOOKING_SOFT_TYPE :
            
                soft_booking = self.booking_set.filter(
                date_start__lt = booking_timeslot.date_stop, 
                date_stop__gt = booking_timeslot.date_start,
                booking_type = cur_booking_type)[0]
                
                #send an email to tell the persons that their room
                #isn't available anymore
                if DEBUG:
                    #this is to avoid spamming people while testing the feature
                    print("dummy email to %s"%(soft_booking.email))
                else:
                    pw = raw_input("PW: ")
                    user = raw_input("user: ")
                    send_email(pw,soft_booking.email,"You have been hard booked","Sorry",user) 
                    
                #procede to the deletion of the soft booking
                soft_booking.delete()
                
            elif cur_booking_type == BOOKING_HARD_TYPE:
                proceed_to_booking = False
            
            if proceed_to_booking:
                #the room isn't already hard booked
                self.booking_set.create(
                                    date_start=booking_timeslot.date_start,
                                    date_stop=booking_timeslot.date_stop,
                                    booking_type = BOOKING_HARD_TYPE)
                
                #keep a record of the hard booking made
                of = open(LOG_FILE_NAME,'a')
                of.write("%s,\t"%(timezone.now()))
                of.write("%s,\t"%(self.name))
                of.write("%s,\t"%(booking_timeslot))
                of.write("%s,\t"%("BANNER"))
                of.write("HARD booking,\n")
                of.close() 
                return 0
                
            else:
                return 1
        else:
            raise TypeError("the timeslot instance is not of the right type")


import hashlib

class Booking(models.Model):
    
    classroom = models.ForeignKey(
        Classroom, on_delete=models.CASCADE, null=True)
    date_start = models.DateTimeField(default=timezone.now)
    date_stop = models.DateTimeField(default=timezone.now)

    email = models.EmailField(default="abc@mail.mcgill.ca")

    booking_type = models.IntegerField(default = BOOKING_SOFT_TYPE)

#    def __init__(self,*args,**kwargs):
#        if 'email' in kwargs:
#            print(kwargs['email'])
#        super(Booking,self).__init__(*args,**kwargs)
#        
            

    def __str__(self):
        return "%s to %s by %s" % (
            self.date_start.strftime("%Y-%m-%d from %H:%M"),
            self.date_stop.strftime("%H:%M"),
            self.email)

    def display(self):
        return self.__str__()
    
    def display_timeslot(self):
        return "%s to %s" % (
            self.date_start.strftime("%Y-%m-%d from %H:%M"),
            self.date_stop.strftime("%H:%M"))

    def reminder(self):
        """this function should send a reminder to the person who booked the meeting"""

    def cancel(self):
        """
        this function should send an email to the person who made the booking to to tell them it has been cancelled
        it should then delete the booking                
        """
        
        #I need to work out the encrypting of the email of the person or the booking reference 
        #(I should generate a booking unique key with the email and timeslot)
        salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:5]

        useremail = self.email
#        if isinstance(useremail, unicode):
#        useremail = useremail.encode('utf8')
        act_key= "23jsjsnb652jss394h5h595n0"#hashlib.sha1(salt+useremail).hexdigest()
        
        link=u"http://127.0.0.1:8000/activate/%s"%(act_key)
        send_email(pw,useremail,"activation",link,"pfduc87")     
        
        



class RandomUser(models.Model):

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True)
    email = models.EmailField()

    def __str__(self):
        return self.email
