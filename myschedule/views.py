from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from account.models import Profile
from .forms import MyTimetableForm,MyCalendarForm
from .models import MyTimetable,MyCalendar
from django.views.decorators.csrf import csrf_exempt
from django.contrib.humanize.templatetags.humanize import naturaltime

from django.db.models import Q
import json

def TimetableView(request):
    form = MyTimetableForm()
    user = Profile.objects.get(user_p = request.user)
    timetables = MyTimetable.objects.filter(timetable_by=user)
    if request.method == 'POST':
         #pass form for validation
        
        form = MyTimetableForm(request.POST)
        #if form is valid and cleaned
        if form.is_valid():
        #save form, login user and redirect user to profile page
            
            user = Profile.objects.get(user_p = request.user)
            timetable = form.save(commit=False)  
            timetable.timetable_by = user  
            timetable.save()
            
            return redirect('timetable')
            
        else:
            
            return render(request,'account/myschedule/timetable.html',{'form':form,'timetables':timetables})
    
    return render(request,'account/myschedule/timetable.html',{'form':form,'timetables':timetables})


def MycalendarView(request):
    form = MyCalendarForm()
    user = Profile.objects.get(user_p = request.user)
    mycalendars = MyCalendar.objects.filter(calendar_by=user)
    if request.method == 'POST':
         #pass form for validation
        
        form = MyCalendarForm(request.POST)
        #if form is valid and cleaned
        if form.is_valid():
        
        #save form, login user and redirect user to profile page
            user = Profile.objects.get(user_p = request.user)
            timetable = form.save(commit=False)  
            timetable.calendar_by = user  
            timetable.save()
            
            return redirect('mycalendar')
            
        else:
            
            return render(request,'account/myschedule/mycalendar.html',{'form':form,'mycalendars':mycalendars})
    
    return render(request,'account/myschedule/mycalendar.html',{'form':form,'mycalendars':mycalendars})



#edit project view    
def EditTimetableView(request,timetable_id):
    timetable = MyTimetable.objects.get(pk = timetable_id)
    forms = MyTimetableForm()
    edittimetable = "POST"
    form = MyTimetableForm(instance = timetable)
    if request.method == "POST" :
        form = MyTimetableForm(request.POST, request.FILES,instance = timetable)
        if form.is_valid():
            
            form.save()
            return redirect('timetable')
        else:
            return render(request,'account/editpage.html',{'form':form,'edittimetable':edittimetable})

    return render(request,'account/editpage.html',{'timetable':timetable,'form':form,'forms':forms,'edittimetable':edittimetable})



#delete project view
def DeleteTimetableView(request):
    
   
    if request.method == 'POST':
        timetable = request.POST.get('delete')
        project = MyTimetable.objects.get(pk = timetable)
        
        project.delete()
        
        
        
        return redirect('timetable')
    return redirect('timetable')  
    
    
    
#edit project view    
def EditCalendarView(request,calendar_id):
    calendar = MyCalendar.objects.get(pk = calendar_id)
    forms = MyCalendarForm()
    editmycalendar = "POST"
    form = MyCalendarForm(instance = calendar)
    if request.method == "POST" :
        form = MyCalendarForm(request.POST, request.FILES,instance = calendar)
        if form.is_valid():
            
            form.save()
            return redirect('mycalendar')
        else:
            return render(request,'account/editpage.html',{'calendar':calendar,'form':form,'editmycalendar':editmycalendar})

    return render(request,'account/editpage.html',{'calendar':calendar,'form':form,'forms':forms,'editmycalendar':editmycalendar})



#delete project view
def DeleteCalendarView(request):
    
   
    if request.method == 'POST':
        timetable = request.POST.get('delete')
        project = MyCalendar.objects.get(pk = timetable)
        
        project.delete()
        
        
        
        return redirect('mycalendar')
    return redirect('mycalendar')      