from django.test import TestCase

from django.utils import timezone
from django.test import TestCase

from .models import Booking


class BookingMethodTests(TestCase):

    def booking_was_made_in_the_past(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is in the future.
        """
        pass
