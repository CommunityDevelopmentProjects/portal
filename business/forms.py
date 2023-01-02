from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from phonenumber_field.formfields import PhoneNumberField
from django.urls import reverse_lazy
from django.contrib.auth import login,authenticate,logout
from .models import Products,Orders

User = get_user_model()


class createProductForm(forms.ModelForm):
    product_images = forms.ImageField(required=False,widget = forms.FileInput(attrs={'multiple':True}))
    class Meta:
        model=Products
        fields = ['product_brand_name','product_generic_name','product_packaging','product_color',
        'product_quantity','product_old_price','product_price','product_description','product_availability']

                      
class ProductImageForm(forms.Form):
    #image1 = forms.ImageField(label = 'Select Images',widget = forms.FileInput(attrs={'multiple':True}),)
    image1 = forms.ImageField(label = 'Select Image1',required = False)
    image2 = forms.ImageField(label = 'Select Image2',required = False)
    image3 = forms.ImageField(label = 'Select Image3',required = False)
        
        
class ConfirmOrderForm(forms.ModelForm):

    class Meta:
        model=Orders
        fields = ['order_transaction_id','order_payement_mode','amount_paid']
        