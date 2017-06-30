from django.test import TestCase

from django.utils import timezone

from .models import Classroom, BOOKING_FREE_TYPE, \
                    BOOKING_SOFT_TYPE, BOOKING_HARD_TYPE

from .date_play import TimeSlot


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
            TimeSlot(datestr, datestr = True)

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
                                       date_stop = ts.date_stop,
                                       email = "soft.test@mcgill.ca")
        
        self.cr.save()


    def test_is_booked_method_conflict_end_during_existing_with(self):
        
        ts=TimeSlot("2016-05-02 from 08:00 to 09:30", datestr = True)        
        
        self.assertEqual(self.cr.is_booked(ts), True)
        
    def test_is_booked_method_conflict_start_during_existing_booking(self):
        
        ts=TimeSlot("2016-05-02 from 09:10 to 10:30", datestr = True)        
        
        self.assertEqual(self.cr.is_booked(ts), True)
   
    def test_is_booked_conflict_overlap_existing_booking(self):
        
        ts=TimeSlot("2016-05-02 from 08:10 to 10:30", datestr = True)        
        
        self.assertEqual(self.cr.is_booked(ts), True)
        
    def test_is_booked_booking_starts_exactly_when_existing_booking_stops(self):
        
        ts=TimeSlot("2016-05-02 from 13:00 to 14:00", datestr = True)        
        
        self.assertEqual(self.cr.is_booked(ts), False)
        
    def test_is_booked_booking_stops_exactly_when_existing_booking_starts(self):
        
        ts=TimeSlot("2016-05-02 from 08:00 to 09:00", datestr = True)        
        
        self.assertEqual(self.cr.is_booked(ts), False)
        
    def test_make_soft_booking_soft_booking_timeslot_already_exists(self):
        ts = TimeSlot(date = timezone.now() + timezone.timedelta(1), duration = 1)
        self.cr.make_soft_booking(ts, "soft.test@mcgill.ca")
        with self.assertRaises(ValueError):
            self.cr.make_soft_booking(ts, "soft.test@mcgill.ca")
     
        
    def test_make_soft_booking_booking_timeslot_is_free(self):
        
        ts = TimeSlot(date = timezone.now() + timezone.timedelta(1), duration = 1)       
        num_previous_bookings = len(self.cr.booking_set.all())
        
        self.cr.make_soft_booking(ts, "soft.test@mcgill.ca")
        num_current_bookings = len(self.cr.booking_set.all())

        self.assertEqual(num_previous_bookings+1,num_current_bookings)
        
    def test_make_hard_booking_soft_booking_timeslot_already_exists(self):
        
        ts=TimeSlot("2016-05-02 from 09:00 to 10:00", datestr = True)        
        num_previous_bookings = len(self.cr.booking_set.all())
        num_previous_soft_bookings = len(self.cr.booking_set.filter(
                                        booking_type = BOOKING_SOFT_TYPE))        
        
        num_previous_hard_bookings = len(self.cr.booking_set.filter(
                                        booking_type = BOOKING_HARD_TYPE))        
        
        self.cr.make_hard_booking(ts)
        
        num_current_bookings = len(self.cr.booking_set.all())
        num_current_soft_bookings = len(self.cr.booking_set.filter(
                                        booking_type = BOOKING_SOFT_TYPE))        
        
        num_current_hard_bookings = len(self.cr.booking_set.filter(
                                        booking_type = BOOKING_HARD_TYPE))
        
        #the hardbooking should destroy the soft booking existing
        self.assertEqual(num_previous_bookings,num_current_bookings) 
        
        self.assertEqual(num_previous_soft_bookings - 1,
                         num_current_soft_bookings)  
        
        self.assertEqual(num_previous_hard_bookings + 1,
                         num_current_hard_bookings) 

        
    def test_make_hard_booking_booking_timeslot_is_free(self):
        
        ts=TimeSlot("2016-05-02 from 15:00 to 17:00", datestr = True)        
        num_previous_bookings = len(self.cr.booking_set.all())
        
        self.cr.make_hard_booking(ts)
        num_current_bookings = len(self.cr.booking_set.all())

        self.assertEqual(num_previous_bookings+1,num_current_bookings)
        

    def test_flush_past_bookings(self):
        current_ts = TimeSlot(date = timezone.now() + timezone.timedelta(1),
                              duration=1)
        
        past_ts = TimeSlot(date = timezone.now() - timezone.timedelta(1),
                              duration=1)
            
        self.cr.booking_set.create(date_start = current_ts.date_start,
                                   date_stop = current_ts.date_stop,
                                   email = "soft.test@mcgill.ca")
                                   
        self.cr.booking_set.create(date_start = past_ts.date_start,
                                   date_stop = past_ts.date_stop,
                                   email = "soft.test@mcgill.ca")
        
        self.cr.flush_past_bookings()        
        
        num_current_bookings = len(self.cr.booking_set.all())
        
        self.assertEqual(num_current_bookings,1)
        
    def test_adjacent_soft_booking_merge(self):
        # test merging between two consecutive bookings
        ts = TimeSlot(date = timezone.now() + timezone.timedelta(1), duration = 1)
        ts2 = TimeSlot(date = ts.date_stop, duration = 1)
        num_previous_bookings = len(self.cr.booking_set.all())
        
        self.cr.make_soft_booking(ts, "soft.test@mcgill.ca")
        self.cr.make_soft_booking(ts2, "soft.test@mcgill.ca")
        num_current_bookings = len(self.cr.booking_set.all())

        self.assertEqual(num_previous_bookings + 1, num_current_bookings)
        
    def test_adjacent_soft_booking_merge_sandwich(self):
        # test merging for when new booking is sandwiched between two old ones
        ts = TimeSlot(date = timezone.now() + timezone.timedelta(1), duration = 1)
        ts2 = TimeSlot(date = ts.date_stop, duration = 1)
        ts3 = TimeSlot(date = ts2.date_stop, duration = 1)
        num_previous_bookings = len(self.cr.booking_set.all())
        
        self.cr.make_soft_booking(ts, "soft.test@mcgill.ca")
        self.cr.make_soft_booking(ts2, "soft.test@mcgill.ca")
        self.cr.make_soft_booking(ts3, "soft.test@mcgill.ca")
        num_current_bookings = len(self.cr.booking_set.all())

        self.assertEqual(num_previous_bookings + 1, num_current_bookings)
        
    def test_adjacent_soft_booking_merge_sandwich2(self):
        # test merging for when new booking is sandwiched between two old ones 2
        ts = TimeSlot(date = timezone.now() + timezone.timedelta(1), duration = 1)
        ts2 = TimeSlot(date = ts.date_stop, duration = 1)
        ts3 = TimeSlot(date = ts2.date_stop, duration = 1)
        
        self.cr.make_soft_booking(ts, "soft.test@mcgill.ca")
        self.cr.make_soft_booking(ts3, "soft.test@mcgill.ca")
        num_previous_bookings = len(self.cr.booking_set.all())
        self.cr.make_soft_booking(ts2, "soft.test@mcgill.ca")
        num_current_bookings = len(self.cr.booking_set.all())
        self.assertEqual(num_previous_bookings - 1, num_current_bookings)
        
    def test_past_time_booking(self):
        # make sure it is impossible to book past times
        past_ts = TimeSlot(date = timezone.now() - timezone.timedelta(2), duration = 1)
        with self.assertRaises(ValueError):
            self.cr.make_soft_booking(past_ts, "soft.test@mcgill.ca")        
        
#    def test_modify_booking(self):
#        
#        ts=TimeSlot("2016-05-02 from 15:00 to 17:00", datestr = True)        
##        num_previous_bookings = len(self.cr.booking_set.all())
#        
#        self.cr.make_soft_booking(ts,"pierre-francois.duc@mail.mcgill.ca")
#        
#        ts=TimeSlot("2016-05-02 from 19:00 to 21:00", datestr = True)        
##        num_previous_bookings = len(self.cr.booking_set.all())
#        
#        self.cr.make_soft_booking(ts,"pierre-francois.duc@mail.mcgill.ca")        
#        
#        booking = self.cr.booking_set.filter(email = "pierre-francois.duc@mail.mcgill.ca")
#        print(booking)
#        booking[0].cancel()