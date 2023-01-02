from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from phonenumber_field.formfields import PhoneNumberField
from django.urls import reverse_lazy
from django.contrib.auth import login,authenticate,logout
from .models import Support_Accounts,Support_Accounts_transactions

User = get_user_model()

                
class createSupportAccountForm(forms.ModelForm):
    images = forms.ImageField(required=False,widget = forms.FileInput(attrs={'multiple':True}))
    class Meta:
        model=Support_Accounts
        fields = ['account_name','call_to_action','button_text','needed_amount','description','account_status','display_total_status']


class SupportAccountForm(forms.ModelForm):
    images = forms.ImageField(required=False,widget = forms.FileInput(attrs={'multiple':True}))
    class Meta:
        model=Support_Accounts_transactions
        fields = ['support_amount']

class TreasurerConfirmSupportAccountForm(forms.ModelForm):
    
    class Meta:
        model=Support_Accounts_transactions
        fields = ['payement_mode','transaction_id','support_paid']