# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 18:05:06 2017

@author: pfduc
"""

class BookingError(Exception):
   def __init__(self, arg):
      self.message = arg
      
class TimeSlotError(BookingError):
   def __init__(self, arg):
      self.message = arg