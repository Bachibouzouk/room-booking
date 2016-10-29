from django.conf.urls import url

from . import views

app_name='room_display'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^availablerooms/$', views.availableroomsview, name='available_rooms'),
    url(r'^user/(?P<user_name>.+)/$', views.userview, name='user_view'),
    url(r'^activate/(?P<key>.+)$', views.modify_booking_view, name = 'modify_booking_view'),
    url(r'^(?P<room_name>.+)/confirm_booking/$', views.confirmbookingview, name = 'confirm_booking_view'),
    url(r'^(?P<room_name>.+)/$', views.roomview, name='room_view'),  #    url(r'^(?P<room_name>.+)/(?P<time>.+)$', views.roomview, name='room_view'),    
]
