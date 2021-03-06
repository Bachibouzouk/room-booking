from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpRequest
from django.template import loader
from django.shortcuts import render, redirect, get_object_or_404

from django.utils import timezone

from .date_play import get_month_dates, get_next_seven_days, timeslots, TimeSlot, append_timeslot, booking_step

from django.core.urlresolvers import reverse

from .models import Classroom, Booking, Calendar, SelectDateTime, CancelBooking

from django.views import generic

from .email_management import send_encrypted_link, check_encription

import hashlib
import uuid
from .room_booking_exception import BookingError, TimeSlotError

"""
using the function render() to do the same thing as loading the template



def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)
"""


class IndexView(generic.ListView):
    template_name = 'room_display/index.html'
    context_object_name = 'room_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Classroom.objects.all()

# class RoomView(generic.DetailView):
#    model = Classroom
#    template_name = 'room_display/room_view.html'


def roomview(request, room_name, counter_day=None, counter_time=None, time=None):
#    import ipdb; ipdb.set_trace()
    print("Room_view")
    print(request)
    try:
        room = Classroom.objects.get(name=room_name)

        # collect all the bookings made for that room
        booking_list = room.booking_set.all()

        # generate the calendar for future booking
        dates, weekdays, booktime_list = get_next_seven_days()

        # works out what time period is already booked
        conflict_list = room.is_booked(booktime_list)

        if not time == None:
            timeslot = time
        else:
            timeslot = None


        if request.method == 'POST':
            query_dict = dict(request.POST)

            print(query_dict)

            if "booking_slot" in query_dict.keys():

		#this needs to be in confirm booking view
                requested_bookings = request.POST.getlist("booking_slot")
                # append the timeslots together if they are concomittent
                booking_timeslots = append_timeslot(requested_bookings)

                if "email" in query_dict.keys():
                    email = request.POST["email"]

                return render(request, 'room_display/confirm_booking_view.html',
                  {"room": room, "booking_timeslots": booking_timeslots,"email": email})

            elif "clear bookings" in query_dict.keys():
                """ this should be removed in the published version """
                room.booking_set.all().delete()


    except Classroom.DoesNotExist:
        raise Http404("Room does not exist :" + str(room_name))
        
        
    return render(request, 'room_display/room_view.html',
                  {'room': room, 'booking_list': booking_list, 'dates': dates,
                   'weekdays': weekdays, "timeslots": timeslots,
                   "timeslot": timeslot, "booktime_list": [zip(bl, cl) for bl, cl in zip(booktime_list, conflict_list)]})


def userview(request,user_name):
    """This view should get a room name and a time (and an email),create a booking and assign it to the room"""
    
    print(user_name)    

    bk = Booking.objects.filter(email = user_name)
    print(bk)
    return render(request, 'room_display/user_view.html', {'user_name': user_name,
                                                           'booking_list': bk})



def modify_booking_view(request, hashed_key = None):
    """
        this view should be accessible from cancel booking button next to each 
        booking, it could also be accessible as a logon page, ie a user enters
        their email address and click a button to send an authentication email 
        to their email inbox.
        
        The possibility to cancel one particular booking should be possible as
        well as seeing and managing all reservations (authentication scheme)
        One possible scheme would be to use a random booking associated with
        the user as a salt for encryption and add more information than just 
        the email, for example email plus '101' for access one booking or '100'
        for all bookings. Tests should be implemented for that purpose. (we can
        fake the click by using the hashed_key to redirect to the view)
    """

    #for the view before authentication procedure (user need to identify)
    if hashed_key is None:
        
        #If the user sent their email address through the click
        if request.method == 'POST':
            
            query_dict = dict(request.POST)
            print("In modify (POST) now")
            print(query_dict)

            #This request comes from a particular set of bookings
            if "bk_key" in query_dict.keys():
                bk_key = request.POST["bk_key"]
                booking = Booking.objects.filter(key = bk_key)
                
                if len(booking) > 1:
                    print(booking)
                    raise ValueError("Each booking is supposed to be unique")
                    
                    # we should check that the user is the same and the bookings are next to each other 
                else:
                    
                    booking = booking[0]
            
                       
                if "send_email" in query_dict.keys():
                    
                    sha_key = bk_key
                    title = "Soft-booking modification or cancellation"
                    send_encrypted_link("pfduc@physics.mcgill.ca", booking.email,
                                        title,
                                        sha_key, 
                                        "http://%s/room_display/modify_booking/"%(request.META["HTTP_HOST"]))
            
            #if the user clicked on "modify/cancel button on the index
            if "send_email" in query_dict.keys():
                
                print("There is an email in the post querydict")
                #see comment in the description of the fonction
            
        #if the user clicked on "cancel booking button" next to a booking
        elif request.method == 'GET':
            
            modify_form = CancelBooking()
            
    #this is valid if the user clicked on the link sent to their email inbox        
    else:
        
        all_bookings = Booking.objects.all()
        booking = None
        
        #browse through all bookings to find the corresponding one
        
        for bk in all_bookings:
            
            salt = bk.key
            
            information = "%s"%(bk.email)
            print(salt)
            print(information)
            
            if check_encription(hashed_key,information,salt):
                print("victory")
                
                timeslot = bk.display_timeslot()
                email = bk.email
                bk.delete()

    return render(request, 'room_display/modify_booking.html', locals())


def confirmbookingview(request, room_name): 
    try:
        #get the room in the DB by its name
        room = Classroom.objects.get(name=room_name)

        #the way to get to this page is only through the POST method
        if request.method == 'POST':
            query_dict = dict(request.POST)
            print("Confirm Booking View")
            print(request)
            print(query_dict)
            print("")

        
            if "booking_slot" in query_dict.keys():
                #fetch the requested booking slots
                requested_bookings = request.POST.getlist("booking_slot")
                # append the timeslots together if they are concomittent
                booking_timeslots = append_timeslot(requested_bookings)
            
            else:
                #if the booking timeslots are not present we return to the page
                return redirect("http://%s/room_display/%s" % (request.META["HTTP_HOST"], room.name))
        
            if "email" in query_dict.keys():
                email = request.POST["email"]
            else:
                email = ""
                  
            if "booking_decision" in query_dict.keys():
                #This key is present only if the user pressed on one of the
                #confirm or cancel booking buttons
            
#                if "booking_slot" in query_dict.keys():            
#                    requested_bookings = request.POST.getlist("booking_slot")
#                    
#                    booking_timeslots = append_timeslot(requested_bookings)
                    
                decision = request.POST["booking_decision"]
                
                if decision == "confirmed":
                    # add the bookings to the room
                    #TODO : make sure the booking wasn't already performed
                
                    #this is just for test purpouses
                    if "hard_book" in query_dict.keys():
                        for booking_timeslot in booking_timeslots:
                            room.make_hard_booking(booking_timeslot)
                    else: # soft booking
                        for booking_timeslot in booking_timeslots:
                            try:
                                room.make_soft_booking(booking_timeslot, email)
                            except TimeSlotError as e:
                                return render(request, 
                                    'room_display/confirm_booking_view.html', 
                                    {"room": room, 
                                     "booking_timeslots": booking_timeslots,
                                     "email": email, 
                                     "errorMessage" : e})
                            except BookingError as e:
                                return render(request, 
                                    'room_display/confirm_booking_view.html', 
                                    {"room": room, 
                                     "booking_timeslots": booking_timeslots,
                                     "email": email, 
                                     "errorMessage" : e})
                            except:
                                raise
                                
                elif decision == "cancelled":
                    #do nothing
                    pass
                else:
                    #this should not happend because the method is POST and not GET but one never knows
                   raise Http404("The value of the booking confirmation is not confirmed nor cancelled") 

                #In both cases return to the roomview
                #I couldn't make the f**** redirect function to work with the url name
                return redirect("http://%s/room_display/%s" % (request.META["HTTP_HOST"],room.name))
            
            else:
                #This key is not present then it means we arrived on this page from room_view
                return render(request, 'room_display/confirm_booking_view.html',
                  {"room": room, "booking_timeslots": booking_timeslots,"email": email})
                
        else:
            raise Http404(
            "this page should not be displayed on its own (it needs to be accessed through the 'book' button)")
    except Classroom.DoesNotExist:
        raise Http404("Room does not exist :" + str(room_name))


def availableroomsview(request):
    """the capacity value should be tested to be positive integer"""
    room_list = None
    capacity = None
    timecheck = SelectDateTime()
    requested_datetime = None
    
    try:
        if request.method == 'POST':
            query_dict = dict(request.POST)
            print(query_dict)
            
            #get the full list of the rooms
            room_list = Classroom.objects.all()    
            
            if 'capacity' in query_dict.keys():
                #the user wanted to filter by capacity
                
                capacity = request.POST['capacity']
                if capacity == "":
                    capacity = None
                else:
                    room_list = room_list.filter(number_seats__gte=capacity)
                    
            if 'timestart' and 'timestop' and 'date' in query_dict.keys():
                hourstart = float(request.POST['timestart'])
                hourstop = float(request.POST['timestop'])
                date = timezone.datetime.strptime(request.POST['date'],"%Y-%m-%d")
                
#                if "duration" in query_dict.keys():
#                    duration = float ()
#                import ipdb;ipdb.set_trace()
                try :
                    requested_datetime = TimeSlot(date, hourstart, 
                                                  duration = hourstop - hourstart)
    #                print(requested_datetime)
                    cr = room_list
                    good_cr =[]
                    for c in cr:
                        if c.is_booked(requested_datetime):
                            pass
                        else:
                            good_cr.append(c)
                    room_list = good_cr
                except ValueError:
                    requested_datetime = "inconsistent"
                    print("Fuck you value error, fuck you") # made me laugh when I read this
				#print(room_list)
				
			# try to make the fields remember what was the inputs last time
            timecheck.fields['date'].initial = request.POST['date']
            timecheck.fields['timestart'].initial = hourstart
            timecheck.fields['timestop'].initial = hourstop
			

        elif request.method == 'GET':
            #get the full list of the rooms
            room_list = Classroom.objects.all()


    except Classroom.DoesNotExist:
        raise Http404(
            "The classroom you are looking for doesn't exist")
            
#    except ValueError or KeyError:
#        capacity = "ValueError"
#        room_list = None
#    else:
#        capacity = "None"
#        room_list = None
#        timecheck=SelectDateTime()
#    if capacity == None:
#            capacity = "None"
#    calendar = Calendar()
    
    return render(request, 'room_display/available_rooms_view.html', 
                          {"room_list": room_list, 
                          "capacity": capacity, 
                          "time_slot": requested_datetime,
                          "timecheck": timecheck})
