from django.conf.urls import url

from . import views

app_name='room_display'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^availablerooms/$', views.availableroomsview, name='available_rooms'),
    url(r'^booking/$', views.makebookingview, name='make_booking'),
    url(r'^(?P<room_name>.+)/$', views.roomview, name='room_view'),    
    url(r'^(?P<room_name>.+)/(?P<time>.+)$', views.roomview, name='room_view'),    
]
