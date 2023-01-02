from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('timetable/',views.TimetableView,name ='timetable'),
    path('edittimetable/<timetable_id>/',views.EditTimetableView,name ='edittimetable'),
    path('deletetimetable/',views.DeleteTimetableView,name ='deletetimetable'),
    
    
    
    path('mycalendar/',views.MycalendarView,name ='mycalendar'),
    path('editmycalendar/<calendar_id>/',views.EditCalendarView,name ='editmycalendar'),
    path('deletemycalendar/',views.DeleteCalendarView,name ='deletemycalendar'),
    ]