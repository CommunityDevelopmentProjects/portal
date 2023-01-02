from django.urls import path
from . import views


urlpatterns = [
   
    path('signup/',views.RegisterUser,name ='signup'),
    path('',views.UserProfile,name ='profile'),
    path('login/',views.login_user,name ='login'),
    path('logout/',views.LogoutView,name ='logout'),
    path('editp/',views.EdituserView,name ='editp'),
    
    
    path('addproject/',views.AddProjectView,name ='addproject'),
    path('editproject/<project_id>',views.EditProjectView,name ='editproject'),
    path('deleteproject',views.DeleteProjectView,name ='deleteproject'),
    
  
    path('themesettings/',views.ThemeSettingsView,name ='themesettings'),
   
   
]