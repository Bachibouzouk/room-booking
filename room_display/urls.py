from django.conf.urls import url

from . import views

app='room_display'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    #url(r'^$', views.index, name='index'),
   # url(r'^(?P<room_pk>)/$', views.RoomView.as_view(), name='room_view'),
    url(r'^(?P<room_name>.+)/$', views.roomview2, name='room_view_notgen')
]
