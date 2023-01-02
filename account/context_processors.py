from django.contrib.auth.decorators import login_required
from account.models import Profile
from community.models import association_member
from business.models import Orders
from feed.models import Posts
from django.db.models import Q
import datetime
def active_user(request):
    active_user = []
    active_group = []
    my_groups = []
    mycart_count = []
    post_no = 0
    date_today =  datetime.datetime.now() 
    if request.user.is_authenticated:
                 
        active_user = Profile.objects.get(user_p = request.user)
        my_groups = association_member.objects.filter(member = active_user)
        mycart_count = Orders.objects.filter(order_by =active_user,buyer_status = False).count()
       
        if 'activegroup' in request.session:
            post_no = Posts.objects.filter(Q(posted_to =request.session['activegroupbackend']) ).count()
            try:
            
                active_group = association_member.objects.get(pk = request.session['activegroup'])
            except:
                pass
            
    return{'post_no':post_no,'mycart_count':mycart_count,'date_today':date_today,'my_groups':my_groups,'active_user':active_user,'active_group':active_group}
    
    #OTHER DEFS WILL RETURN DICTIONARY LIKE CONTEXTS