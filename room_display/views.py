from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.shortcuts import render, get_object_or_404

from .date_play import get_month_dates, get_next_seven_days, timeslots, TimeSlot, append_timeslot, booking_step

from django.core.urlresolvers import reverse

from .models import Classroom, Booking, Calendar, SelectDateTime

from django.views import generic
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

    try:
        room = Classroom.objects.get(name=room_name)

        if request.method == 'POST':

            query_dict = dict(request.POST)
            print(query_dict)
            if "Book" in query_dict.keys():
                requested_bookings = request.POST.getlist("Book")

                # append the timeslots together if they are concomittent
                booking_timeslots = append_timeslot(requested_bookings)

                if "Email" in query_dict.keys():
                    email = request.POST["Email"]

                # add the bookings to the room
                for booking_timeslot in booking_timeslots:
                    room.booking_set.create(
                        date_start=booking_timeslot.date_start,
                        date_stop=booking_timeslot.date_stop,
                        email=email)

            elif "clear bookings" in query_dict.keys():
                """ this should be removed in the published version """
                room.booking_set.all().delete()

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
    except Classroom.DoesNotExist:
        raise Http404("Room does not exist :" + str(room_name))
    return render(request, 'room_display/room_view.html',
                  {'room': room, 'booking_list': booking_list, 'dates': dates,
                   'weekdays': weekdays, "timeslots": timeslots,
                   "timeslot": timeslot, "booktime_list": [zip(bl, cl) for bl, cl in zip(booktime_list, conflict_list)]})


def makebookingview(request):
    """This view should get a room name and a time (and an email),create a booking and assign it to the room"""
    return render(request, 'room_display/make_booking_view.html', {})


def availableroomsview(request):
    """the capacity value should be tested to be positive integer"""

    try:
        if request.method == 'POST':
            query_dict = dict(request.POST)
            print(query_dict)
            if "capacity" in query_dict.keys():
                capacity = request.POST['capacity']
                room_list = Classroom.objects.filter(
                    number_seats__gte=capacity)

            """
            here I should find a quick way to to make a datetime object with
            {'day': ['1'], 'hour': ['10'], 'min': ['00'], 'duration': ['1'], 'year': ['2016'], 'month': ['5']}
           
           
           then I would look throught the DB for all rooms that aren't booked
            at this time using the is_booked method
            
            OR
            
            I can see which are the bookings which are within the time period
            and then find the list of the room available with the total list minus
            the booked rooms
            """

    except Classroom.DoesNotExist:
        raise Http404(
            "There is no room with number of seats greater than :" + str(capacity))
    except ValueError or KeyError:
        capacity = "ValueError"
        room_list = None
    else:
        capacity = "None"
        room_list = None
#    if capacity == None:
#            capacity = "None"
#    calendar = Calendar()
    timecheck=SelectDateTime()
    return render(request, 'room_display/available_rooms_view.html', {"room_list": room_list, "capacity": capacity, "step_time": booking_step,"timecheck":timecheck})
