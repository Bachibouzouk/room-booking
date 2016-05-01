from django.test import TestCase

from django.utils import timezone
from django.test import TestCase


from .models import Classroom, Booking

from .date_play import TimeSlot,get_next_seven_days


class TimeSlotMethodTests(TestCase):
    
    def setUp(self):
        self.datestr = "2016-05-02 from 09:00 to 10:00"
        self.duration_str = 1
        self.date = "2016-03-02 from 04:00 to 05:00"
        self.ts_str = TimeSlot(self.datestr,datestr=True)
        self.ts = TimeSlot(
            date = timezone.datetime(2016,3,2,4,0,0,tzinfo=timezone.utc),
            duration=1)
    
    def test_create_a_time_slot_from_date_and_duration(self):
        self.assertEqual(self.date,"%s"%(self.ts))
    
    def test_create_a_time_slot_from_string(self):
        self.assertEqual(self.datestr,self.ts_str.__str__())
        
    def test_create_a_time_slot_from_string_and_get_the_right_duration(self):
        self.assertEqual(self.duration_str,self.ts_str.duration)
        
    def test_create_a_time_slot_from_string_switch_start_stop(self):
        datestr="2016-05-02 from 10:00 to 09:00"
        with self.assertRaises(ValueError):
            TimeSlot(datestr,datestr=True)

    def test_instance_print(self):
        self.assertEqual(self.datestr,"%s"%(self.ts_str))
        self.assertEqual(self.date,"%s"%(self.ts))
        
    def test_add_method(self):
        combined_ts_str = "2016-05-01 from 09:00 to 11:00"
        ts1=TimeSlot("2016-05-01 from 09:00 to 10:00",datestr=True)
        ts2=TimeSlot("2016-05-01 from 10:00 to 11:00",datestr=True)
        
        self.assertEqual("%s"%(ts1+ts2), combined_ts_str)
        
        self.assertEqual("%s"%(ts1+self.duration_str), combined_ts_str)
 
        
    

class ClassRoomMethodTests(TestCase):

    def setUp(self):
        self.cr = Classroom.objects.create(name="TEST",
                                           location="TEST",
                                           number_seats=70)
        self.cr.save()
        timeslots=[TimeSlot("2016-05-02 from 09:00 to 10:00",datestr=True),
                   TimeSlot("2016-05-02 from 11:00 to 13:00",datestr=True),
                   TimeSlot("2016-05-03 from 11:00 to 13:00",datestr=True)]
                      
        
        for ts in timeslots:
            self.cr.booking_set.create(date_start = ts.date_start,
                                       date_stop = ts.date_stop)
        
        self.cr.save()


    def test_is_booked_method_conflict_end_during_existing_with(self):
        
        ts=TimeSlot("2016-05-02 from 08:00 to 09:30",datestr=True)        
        
        self.assertEqual(self.cr.is_booked(ts),True)
        
    def test_is_booked_method_conflict_start_during_existing_booking(self):
        
        ts=TimeSlot("2016-05-02 from 09:10 to 10:30",datestr=True)        
        
        self.assertEqual(self.cr.is_booked(ts),True)
   
    def test_is_booked_conflict_overlap_existing_booking(self):
        
        ts=TimeSlot("2016-05-02 from 08:10 to 10:30",datestr=True)        
        
        self.assertEqual(self.cr.is_booked(ts),True)
        
    def test_is_booked_booking_starts_exactly_when_existing_booking_stops(self):
        
        ts=TimeSlot("2016-05-02 from 13:00 to 14:00",datestr=True)        
        
        self.assertEqual(self.cr.is_booked(ts),False)
        
    def test_is_booked_booking_stops_exactly_when_existing_booking_starts(self):
        
        ts=TimeSlot("2016-05-02 from 08:00 to 09:00",datestr=True)        
        
        self.assertEqual(self.cr.is_booked(ts),False)