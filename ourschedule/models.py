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
  
    
    

class OurTimetable(models.Model):
    program_by = models.ForeignKey(association,on_delete = models.CASCADE, related_name = 'program_by')  
    
    day_of_the_week = models.CharField(max_length=255,choices = day_choices, default = 'Monday' )
    event = models.CharField(max_length=255)
    description = models.TextField()       
    duration= models.CharField(max_length=255)
    
    date_made = models.DateTimeField(auto_now_add = True) 
    
          
    def __str__(self):
        return str(self.program_by)+'('+self.event+')'


class OurCalendar(models.Model):
    ourcalendar_by = models.ForeignKey(association,on_delete = models.CASCADE, related_name = 'ourcalendar_by')    
  
    event = models.CharField(max_length=255)
    description = models.TextField()  
    event_time = models.CharField(max_length=255)
    date= models.DateField(default=now,)
    
    date_made = models.DateTimeField(auto_now_add = True) 
    
          
    def __str__(self):
        return str(self.ourcalendar_by)+'('+self.event+')'
