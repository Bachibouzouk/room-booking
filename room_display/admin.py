from django.contrib import admin
#from django.conf.urls import patterns
from django.conf.urls import url
from .models import Booking, Classroom
from .urls import urlpatterns
from .views import roomview

# Register your models here.
admin.site.register(Booking)
admin.site.register(Classroom)

#class BookingAdmin(admin.ModelAdmin):
#    list_filter = ('classroom', 'date_start', 'date_stop', 'email', 'booking_type', 'key')
#admin.site.admin_view(roomview)

#
#def get_admin_urls(urls):
#    def get_urls():
#        my_urls = [ 
#        url(r'^room_display/browse_room/(?P<room_name>.+)/$',admin.site.admin_view(roomview) , name='admin_room_view'),  #    url(r'^(?P<room_name>.+)/(?P<time>.+)$', views.roomview, name='room_view'),    
#        ]
#        return  urls + my_urls
#    return get_urls
#print(admin.site.get_urls())
#admin_urls = get_admin_urls(admin.site.get_urls())
#print(admin_urls())
#admin.site.get_urls = admin_urls