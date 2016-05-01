from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.template import loader
from django.shortcuts import render,get_object_or_404

from .date_play import get_month_dates,get_next_seven_days,timeslots,TimeSlot

from django.core.urlresolvers import reverse

from .models import Classroom, Booking

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

#class RoomView(generic.DetailView):
#    model = Classroom
#    template_name = 'room_display/room_view.html'

def roomview(request,room_name,counter_day=None,counter_time=None,time=None):

    if request.method == 'POST':
        requested_bookings = request.POST.getlist("Book")
        for i in requested_bookings:
            print(isinstance(i,TimeSlot))
#        d=request.POST.dict()
#        print(d.keys())
#        print(d["Book"])
            
    try:
        room=Classroom.objects.get(name=room_name)
        booking_list = room.booking_set.all()
        dates,weekdays,booktime_list=get_next_seven_days()
        if not time == None:
            timeslot = time
        else:
            timeslot = None
    except Classroom.DoesNotExist:
        raise Http404("Room does not exist :"+str(room_name))
    return render(request, 'room_display/room_view.html',
                  {'room': room, 'booking_list': booking_list, 'dates': dates,
                  'weekdays': weekdays, "timeslots": timeslots,
                  "timeslot": timeslot,"booktime_list":booktime_list})

def makebookingview(request):
    """This view should get a room name and a time (and an email),create a booking and assign it to the room"""
    return render(request, 'room_display/make_booking_view.html', {})
    
def availableroomsview(request):
    """the capacity value should be tested to be positive integer"""

    try:
        capacity=request.POST['capacity']
        room_list=Classroom.objects.filter(number_seats__gte=capacity)

    except Classroom.DoesNotExist:
        raise Http404("There is no room with number of seats greater than :"+str(capacity))
    except ValueError or KeyError:
        capacity="ValueError"
        room_list=None
    else:
        capacity="None"
        room_list=None
#    if capacity == None:
#            capacity = "None"
    return render(request, 'room_display/available_rooms_view.html', {"room_list":room_list,"capacity":capacity})