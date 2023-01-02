from django.db import models

from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _lazy
from phonenumber_field.modelfields import PhoneNumberField
from imagekit.models import ProcessedImageField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from account.models import Profile
from community.models import association

day_choices = [('Sunday','Sunday'),
    ('Monday','Monday'),('Tuesday','Tuesday')
    ,('Wednesday','Wednesday'),('Thursday','Thursday'),('Friday','Friday'),('Saturday','Saturday')
    ] 
  
    
    

class MyTimetable(models.Model):
    timetable_by = models.ForeignKey(Profile,on_delete = models.CASCADE, related_name = 'timetable_by')    
    day_of_the_week = models.CharField(max_length=255,choices = day_choices, default = 'Monday' )
    event = models.CharField(max_length=255)
    description = models.TextField()       
    duration= models.CharField(max_length=255)
    
    date_made = models.DateTimeField(auto_now_add = True) 
    
          
    def __str__(self):
        return str(self.timetable_by)+'('+self.event+')'


class MyCalendar(models.Model):
    calendar_by = models.ForeignKey(Profile,on_delete = models.CASCADE, related_name = 'calendar_by')    
  
    event = models.CharField(max_length=255)
    description = models.TextField()  
    event_time = models.CharField(max_length=255)
    date= models.DateField(default=now,)
    
    date_made = models.DateTimeField(auto_now_add = True) 
    
          
    def __str__(self):
        return str(self.calendar_by)+'('+self.event+')'
