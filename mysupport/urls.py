from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('opensupportaccounts/',views.OpenSupportAccounts,name ='opensupportaccounts'),
    path('closedsupportaccounts/',views.ClosedSupportAccounts,name ='closedsupportaccounts'),
    path('closesupportaccount/',views.CloseSupportAccountView,name ='closesupportaccount'),
    path('opensupportaccount/',views.OpenSupportAccountView,name ='opensupportaccount'),
    
    path('editsupportaccount/',views.EditSupportAccount,name ='editsupportaccount'),

    path('seteditsupportaccount/',views.SetSupportAccount,name ='seteditsupportaccount'),
    
    path('createsupportaccount/',views.CreateSupportAccount,name ='createsupportaccount'),
    path('setsupport/',views.SetSupportAccount,name ='setsupport'),
    path('supportaccount/',views.SingleSupportAccount,name ='supportaccount'),
    path('offersupportaccount/',views.OfferSupportAccount,name ='offersupportaccount'),
    path('canceloffersupportaccount/',views.CancelOfferSupportAccount,name ='canceloffersupportaccount'),
    path('tconfirmoffer/',views.TreasurerConfirmOffer,name ='tconfirmoffer'),
    path('tconfirmoffersess/',views.TOfferSupportAccountSess,name ='tconfirmoffersess'),
    path('confirmoffer/',views.ConfirmOffer,name ='confirmoffer'),
    
    
    ]