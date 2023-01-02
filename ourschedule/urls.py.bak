from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('ourprogram/',views.TimetableView,name ='ourprogram'),
    path('editourprogram/<timetable_id>/',views.EditTimetableView,name ='editourprogram'),
    path('deleteprogram/',views.DeleteTimetableView,name ='deleteprogram'),
    
    
    
    path('ourcalendar/',views.MycalendarView,name ='ourcalendar'),
    path('editourcalendar/<calendar_id>/',views.EditCalendarView,name ='editourcalendar'),
    path('deleteourcalendar/',views.DeleteCalendarView,name ='deleteourcalendar'),
    ]