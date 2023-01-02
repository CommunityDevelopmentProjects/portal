from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from imagekit.models import ProcessedImageField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

class UserManager(BaseUserManager):
    def create_user(self,phone_number,user_name,password=None):
        if not phone_number:
            raise ValueError('User must have a phone number')
        user = self.model(phone_number=phone_number,user_name=user_name)
        
        user.set_password(password)
        user.save(using=self._db)
        return user
        
        
    def create_staffuser(self,phone_number,user_name,password):
        user= self.create_user(phone_number,user_name,password=password)
        user.staff = True
        user.save(using = self._db)
        return user
        
    def create_superuser(self,phone_number,user_name,password):
        user = self.create_user(phone_number,user_name,password=password)
        user.staff = True
        user.admin = True
        user.save(using= self._db)
        return user
        
        
class User(AbstractBaseUser):
    phone_number = PhoneNumberField(unique = True)
    user_name = models.CharField(max_length = 255)
    is_active = models.BooleanField(default = True)
    staff = models.BooleanField(default = False)
    admin = models.BooleanField(default = False)
    
    
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['user_name']
    objects = UserManager()
    def __str__(self):
        return str(self.phone_number)
    def get_full_name(self):
        return self.user_name
    def get_short_name(self):
        return self.user_name
        
    def has_perm(self,perm,obj=None):
        return True
        
    def has_module_perms(self,app_label):
        return True
        
    @property
    def is_staff(self):
        return self.staff
    
    @property
    def is_admin(self):
        return self.admin
        
        
        
User = get_user_model()
employement_choices = [('At School','At School'),('Employed','Employed'),('Unemployed','Unemployed'),('Self Employed','Self Employed')] 

# Create your models here.
class Profile(models.Model):
    user_p = models.OneToOneField(User,on_delete = models.CASCADE, related_name = 'user_p')
    profile_image = ProcessedImageField(upload_to='media',blank=True, null=True,
                                           
                                           format='JPEG',
                                           options={'quality': 100})
    full_name = models.CharField(max_length=255,null = True,blank = True)
    address = models.CharField(max_length=255,null = True,blank = True)
    business = models.CharField(max_length=40,null = True, blank = True)
    best_skill = models.CharField(max_length=100,null = True, blank = True)
    mobile = models.CharField(max_length=255,null = True,blank = True)
    phone = models.CharField(max_length=255,null = True,blank = True)
    languages = models.CharField(max_length=255,null = True,blank = True)
    employment = models.CharField(max_length=255,choices = employement_choices,null = True,blank = True)
    status = models.CharField(max_length=25,null = True,blank = True)
    email = models.EmailField(null = True,blank = True)
    
   
    first_position = models.CharField(max_length=255,null = True,blank = True)
    first_role = models.CharField(max_length=255,null = True,blank = True)
    first_company = models.CharField(max_length=255,null = True,blank = True)
    first_period = models.CharField(max_length=255,null = True,blank = True)
    first_role_description = models.TextField(null = True,blank = True) 
    
    
    second_position = models.CharField(max_length=255,null = True,blank = True)
    second_role = models.CharField(max_length=255,null = True,blank = True)
    second_company = models.CharField(max_length=255,null = True,blank = True)
    second_period = models.CharField(max_length=255,null = True,blank = True)
    second_role_description = models.TextField(null = True,blank = True) 
    
    
    third_position = models.CharField(max_length=255,null = True,blank = True)
    third_role = models.CharField(max_length=255,null = True,blank = True)
    third_company = models.CharField(max_length=255,null = True,blank = True)
    third_period = models.CharField(max_length=255,null = True,blank = True)
    third_role_description = models.TextField(null = True,blank = True)
    
    
    fourth_position = models.CharField(max_length=255,null = True,blank = True)
    fourth_role = models.CharField(max_length=255,null = True,blank = True)
    fourth_company = models.CharField(max_length=255,null = True,blank = True)
    fourth_period = models.CharField(max_length=255,null = True,blank = True)
    fourth_role_description = models.TextField(null = True,blank = True) 
    
   
    fifth_position = models.CharField(max_length=255,null = True,blank = True)
    fifth_role = models.CharField(max_length=255,null = True,blank = True)
    fifth_company = models.CharField(max_length=255,null = True,blank = True)
    fifth_period = models.CharField(max_length=255,null = True,blank = True)
    fifth_role_description = models.TextField(null = True,blank = True) 
    
    website = models.CharField(max_length=255,null = True,blank = True)
    facebook = models.CharField(max_length=255,null = True,blank = True)
    instagram = models.CharField(max_length=255,null = True,blank = True)
    twitter = models.CharField(max_length=255,null = True,blank = True)
    github = models.CharField(max_length=255,null = True,blank = True)
    tiktok = models.CharField(max_length=255,null = True,blank = True)
    
    subscribe = models.IntegerField(default = 1)

    about_me = models.TextField(null = True,blank = True)  
    
    def __str__(self):
        return str(self.user_p)+'('+str(self.full_name)+')'
        
        
        
# Create your models here.
class Projects(models.Model):
    project_owner = models.OneToOneField(Profile,on_delete = models.CASCADE, related_name = 'project_owner')
    project_image = ProcessedImageField(upload_to='media',blank=True, null=True,
                                           
                                           format='JPEG',
                                           options={'quality': 100})
    project_name = models.CharField(max_length=255)
    clients = models.CharField(max_length=255,null = True,blank = True)
    start_date = models.CharField(max_length=40,null = True, blank = True)
    due_date = models.CharField(max_length=100,null = True, blank = True)
    status = models.CharField(max_length=255,null = True,blank = True)
    
    def __str__(self):
        return str(self.project_owner)+'('+str(self.project_name)+')'        
        
theme_choices = [('light','light'),('dark','dark')]      
class Themesettings(models.Model):
    theme_owner = models.OneToOneField(Profile,on_delete = models.CASCADE, related_name = 'theme_owner')    
    theme_option = models.CharField(max_length = 10,default = 'light',choices = theme_choices)
    
    
    def __str__(self):
        return self.theme_option       