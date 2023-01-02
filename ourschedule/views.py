from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from account.models import Profile
from .forms import MyTimetableForm,MyCalendarForm
from .models import OurCalendar,OurTimetable
from community.models import association
from django.views.decorators.csrf import csrf_exempt
from django.contrib.humanize.templatetags.humanize import naturaltime

from django.db.models import Q
import json

def TimetableView(request):
    form = MyTimetableForm()
    
    timetables = OurTimetable.objects.filter(program_by__pk = request.session['activegroupbackend'])
    if request.method == 'POST':
         #pass form for validation
        community = association.objects.get(pk = request.session['activegroupbackend'])
        form = MyTimetableForm(request.POST)
        #if form is valid and cleaned
        if form.is_valid():
        #save form, login user and redirect user to profile page
            timetable = form.save(commit=False)  
            timetable.program_by = community 
            timetable.save()
            
            return redirect('ourprogram')
            
        else:
            
            return render(request,'account/ourschedule/timetable.html',{'form':form,'timetables':timetables})
    
    return render(request,'account/ourschedule/timetable.html',{'form':form,'timetables':timetables})


def MycalendarView(request):
    form = MyCalendarForm()
    
    mycalendars = OurCalendar.objects.filter(ourcalendar_by__pk = request.session['activegroupbackend'])
    if request.method == 'POST':
         #pass form for validation
        
        form = MyCalendarForm(request.POST)
        #if form is valid and cleaned
        if form.is_valid():
            community = association.objects.get(pk = request.session['activegroupbackend'])
            #save form, login user and redirect user to profile page
            
            timetable = form.save(commit=False)  
            timetable.ourcalendar_by = community 
            timetable.save()
            
            return redirect('ourcalendar')
            
        else:
            
            return render(request,'account/ourschedule/mycalendar.html',{'form':form,'mycalendars':mycalendars})
    
    return render(request,'account/ourschedule/mycalendar.html',{'form':form,'mycalendars':mycalendars})



#edit project view    
def EditTimetableView(request,timetable_id):
    program = OurTimetable.objects.get(pk = timetable_id)
    forms = MyTimetableForm()
    edittimetable = "POST"
    form = MyTimetableForm(instance = program)
    if request.method == "POST" :
        form = MyTimetableForm(request.POST, request.FILES,instance = program)
        if form.is_valid():
            
            form.save()
            return redirect('ourprogram')
        else:
            return render(request,'account/editpage.html',{'program':program,'form':form,'edittimetable':edittimetable})

    return render(request,'account/editpage.html',{'program':program,'form':form,'forms':forms,'edittimetable':edittimetable})



#delete project view
def DeleteTimetableView(request):
    
   
    if request.method == 'POST':
        timetable = request.POST.get('delete')
        project = OurTimetable.objects.get(pk = timetable)
        
        project.delete()
        
        
        
        return redirect('ourprogram')
    return redirect('ourprogram')  
    
    
    
#edit project view    
def EditCalendarView(request,calendar_id):
    ourcalendar = OurCalendar.objects.get(pk = calendar_id)
    forms = MyCalendarForm()
    editmycalendar = "POST"
    form = MyCalendarForm(instance = ourcalendar)
    if request.method == "POST" :
        form = MyCalendarForm(request.POST, request.FILES,instance = ourcalendar)
        if form.is_valid():
            
            form.save()
            return redirect('ourcalendar')
        else:
            return render(request,'account/editpage.html',{'ourcalendar':ourcalendar,'form':form,'editmycalendar':editmycalendar})

    return render(request,'account/editpage.html',{'ourcalendar':ourcalendar,'form':form,'forms':forms,'editmycalendar':editmycalendar})



#delete project view
def DeleteCalendarView(request):
    
   
    if request.method == 'POST':
        timetable = request.POST.get('delete')
        project = OurCalendar.objects.get(pk = timetable)
        
        project.delete()
        
        
        
        return redirect('ourcalendar')
    return redirect('ourcalendar')      