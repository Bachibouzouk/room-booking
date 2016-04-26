from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.template import loader
from django.shortcuts import render,get_object_or_404

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

def roomview2(request,room_name):
	
    try:
        room=Classroom.objects.get(name=room_name)
        booking_list = room.booking_set.all()
    except Classroom.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'room_display/room_view.html', {'room': room,'booking_list':booking_list})
