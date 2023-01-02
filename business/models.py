from  django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField
from imagekit.models import ProcessedImageField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from community.models import association
from account.models import Profile
User = get_user_model()
mode_choices = [('Not Paid','Not Paid'),('Cash','Cash'),('Mobile Money','Mobile Money')
,('Mobile Money and Cash','Mobile Money and Cash'),('Bank','Bank'),('E-Transfer','E-Transfer')]
#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
#Create your models here.
class Business(models.Model):
    business_owner = models.OneToOneField(Profile,on_delete = models.CASCADE, related_name = 'business_owner')
    
    business_assoc1 = models.IntegerField(default = 0) 
    business_assoc2 = models.IntegerField(default = 0) 
    business_assoc3 = models.IntegerField(default = 0)  
 
    shipping_area = models.CharField(max_length = 255,null = True,blank = True)
    shipping_fee = models.CharField(max_length=255,null = True, blank = True)
    
    cover_image = ProcessedImageField(upload_to='media',blank=True, null=True,
                                           processors=[ResizeToFill(500, 500)],
                                           format='JPEG',
                                           options={'quality': 100})
    business_name = models.CharField(max_length = 255)
    business_address = models.CharField(max_length=255)
    business_slogan = models.CharField(max_length=255,null = True, blank = True)
    business_contacts = models.CharField(max_length= 255)
    about_business = models.CharField(max_length=255)
    date_created = models.DateField(auto_now_add = True) 
    def __str__(self):
    
        return str(self.business_name)
        
        
class Products(models.Model):

    business_p = models.ForeignKey(Business,on_delete = models.CASCADE, related_name = 'business_p')
    product_brand_name = models.CharField(max_length=255)
    product_generic_name = models.CharField(max_length=255)
    product_packaging = models.CharField(max_length=255)
    product_quantity = models.CharField(max_length=255)
    product_purchase_price = models.DecimalField(default=0,decimal_places = 1,max_digits=25)
    product_price = models.DecimalField(default=0,decimal_places = 1,max_digits=25)
    product_description = models.TextField()
    product_availability = models.CharField(max_length=255,default='In Stock')
    product_color = models.CharField(max_length=255,null = True,blank = True)
    product_old_price = models.DecimalField(default=0,decimal_places = 1,max_digits=25)
    product_category = models.IntegerField(default = 0)
    product_type = models.CharField(max_length=255,default ='none' )
    image1 = ProcessedImageField(upload_to='media',blank=True, null=True,
                                           processors=[ResizeToFill(1000, 1000)],
                                           format='JPEG',
                                           options={'quality': 100})
    image2 = ProcessedImageField(upload_to='media',blank=True, null=True,
                                           processors=[ResizeToFill(1000, 1000)],
                                           format='JPEG',
                                           options={'quality': 100})
    image3 = ProcessedImageField(upload_to='media',blank=True, null=True,
                                           processors=[ResizeToFill(1000, 1000)],
                                           format='JPEG',
                                           options={'quality': 100})
    date_added = models.DateField(auto_now_add = True)    
    
    def __str__(self):
    
        return self.product_brand_name  


       
        
class Business_Product_Categories(models.Model):
    business_cat = models.ForeignKey(Business,on_delete = models.CASCADE, related_name = 'business_cat')
    business_category = models.IntegerField(default = 0) 
    date_added = models.DateField(auto_now_add = True)    
    
    def __str__(self):
    
        return str(self.id)          
        




class Orders(models.Model):

    order_product= models.ForeignKey(Products,on_delete = models.CASCADE, related_name = 'order_product')
    order_by = models.ForeignKey(Profile,on_delete = models.CASCADE, related_name = 'order_by') 
    quantity = models.CharField(max_length=255)
    price = models.DecimalField(default=0,decimal_places = 1,max_digits=25)
    total_price = models.DecimalField(default=0,decimal_places = 1,max_digits=25)
    total_order_price = models.DecimalField(default=0,decimal_places = 1,max_digits=25)
    amount_paid = models.DecimalField(default=0,decimal_places = 1,max_digits=25)
    balance = models.DecimalField(default=0,decimal_places = 1,max_digits=25)
    buyer_status = models.BooleanField(default = False)
    seller_status = models.BooleanField(default = False)
    recieved_status = models.BooleanField(default = False)
    order_no = models.IntegerField(default = 0)
    order_payement_mode = models.CharField(max_length=255,default = 'Not Paid',choices = mode_choices)
    order_transaction_id = models.CharField(max_length=255,default = 'None')
    date_added = models.DateField(auto_now_add = True)    
    
    def __str__(self):
    
        return str(self.id)  