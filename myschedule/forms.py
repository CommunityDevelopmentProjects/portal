from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from phonenumber_field.formfields import PhoneNumberField
from django.urls import reverse_lazy
from django.contrib.auth import login,authenticate,logout
from .models import MyTimetable,MyCalendar

User = get_user_model()

class MyTimetableForm(forms.ModelForm):
    class Meta:
        model = MyTimetable
        fields = ['day_of_the_week','duration','event','description']


class MyCalendarForm(forms.ModelForm):
    class Meta:
        model = MyCalendar
        fields = ['date','event_time','event','description']
       
                
