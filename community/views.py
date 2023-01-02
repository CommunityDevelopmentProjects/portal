from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .forms import GroupForm,CompleteGroupForm,GroupLeaderForm,AddMemberGroupForm
from django.views.decorators.csrf import csrf_exempt
from .models import association,association_member,association_leader
from account.models import Profile,Projects
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
import json
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your views here.


# Create your views here.
def CreateAssociationView(request):
    
    #assign RegisterForm to variable
    form = GroupForm()
    
    if request.method == 'POST':
         #pass form for validation
        
        form = GroupForm(request.POST)
        #if form is valid and cleaned
        if form.is_valid():
        #save form, login user and redirect user to profile page
            financial_year = form.cleaned_data.get('financial_year')
            user = Profile.objects.get(user_p = request.user)
            try:
                active_assoc = association_member.objects.get(member = user, active_status = 'active')
                active_assoc.active_status = 'inactive'
                active_assoc.save()
                for key in list(request.session.keys()):
                    if not key.startswith("_"): # skip keys set by the django system
                        del request.session[key]
            except:
                pass
            assoc = form.save(commit=False)  
            assoc.founder = user
            
            assoc.save()           
            myassoc = association_member(member = user,myassociation = assoc) 
            
            myassoc.save()
            
            request.session['activegroup'] = myassoc.pk
            request.session['activegroupbackend'] = myassoc.myassociation.pk
            request.session['activefinancialyear'] = myassoc.myassociation.financial_year
            try:
                financial_year = assoc.myassociation.financial_year
                leader = association_leader.objects.get(financial_year =financial_year,associationleader=assoc,leader_status ='Active' )
                           
                request.session['leaders_role'] = leader.leadership_role
            except:
                request.session['leaders_role'] = 0
            myassoc_leader  = association_leader(
            associationleader = myassoc,  financial_year = financial_year,other_position = 'President'
            )
            myassoc_leader.save()           
            
            return redirect('cprofile')
            
        else:
            
            return render (request,'account/community/create.html',{'form':form})
    
    return render(request,'account/community/create.html',{'form':form})
    


def AssociationView(request):
    active_group = association.objects.get(pk = request.session['activegroupbackend'])
    form = CompleteGroupForm(instance = active_group)
    leaders = association_leader.objects.filter(associationleader__myassociation__pk = request.session['activegroupbackend'])
    members_no = association_member.objects.filter(Q(myassociation__pk = request.session['activegroupbackend']), Q(member_status= 'active')).count()
    return render(request,'account/community/profile.html',{'members_no':members_no,'leaders':leaders,'form':form})
    
    
def EditAssociationView(request):
 
    if request.method == 'POST':
         #pass form for validation
        active_group = association.objects.get(pk = request.session['activegroupbackend'])
        form = CompleteGroupForm(request.POST,request.FILES,instance = active_group)
        
        #if form is valid and cleaned
        if form.is_valid():
        #save form, login user and redirect user to profile page
           
            form.save()
            
         
            return redirect('cprofile')
            
        else:
            
            return redirect('cprofile')
    
    return redirect('cprofile')

@login_required(login_url = 'logout')    
def SearchPublicAssociationView(request):
   
    if request.method == 'POST':
       
       messagess = json.loads(request.body)
       request.session['searchpublicassociation'] = messagess
   
    message_list = [{
      
        'message':'success',
      
    }]
   
    return JsonResponse(message_list,safe=False)  
    
@login_required(login_url = 'logout')
def PublicAssociationView(request):
 
  
  
    
    if 'activegroupbackend' in request.session:
        user = Profile.objects.get(user_p = request.user)
        myassocs = association_member.objects.filter(member = user, member_status ='active' )
        if  'searchpublicassociation' in request.session:
            publicassocs = association.objects.filter(Q(privacy = 'Public'), Q(parent = 0)).filter(Q(name__icontains =request.session['searchpublicassociation'])  
            |Q(slogan__icontains =request.session['searchpublicassociation']) |Q(address__icontains =request.session['searchpublicassociation'])
            |Q(about_us__icontains =request.session['searchpublicassociation']) |Q(what_we_do__icontains =request.session['searchpublicassociation']))
            
            del request.session['searchpublicassociation']
            page = request.GET.get('page',1)
            paginator = Paginator(publicassocs,8)
            try:
                allpublicassocs = paginator.page(page)
            except PageNotAnInteger:
                allpublicassocs = paginator.page(1)
            except EmptyPage:
                allpublicassocs= paginator.page(paginator.num_pages)
        else:
            publicassocs = association.objects.filter(Q(privacy = 'Public'), Q(parent = 0))
            page = request.GET.get('page',1)
            paginator = Paginator(publicassocs,8)
            try:
                allpublicassocs = paginator.page(page)
            except PageNotAnInteger:
                allpublicassocs = paginator.page(1)
            except EmptyPage:
                allpublicassocs = paginator.page(paginator.num_pages) 
    else:
        return redirect('logout')
    return render(request,'account/community/publiccommunities.html',{'myassocs':myassocs,'allpublicassocs':allpublicassocs})

@login_required(login_url = 'logout')    
def SearchMyAssociationView(request):
   
    if request.method == 'POST':
       
       messagess = json.loads(request.body)
       request.session['searchmyassociation'] = messagess
   
    message_list = [{
      
        'message':'success',
      
    }]
   
    return JsonResponse(message_list,safe=False) 
    
@login_required(login_url = 'logout')     
def MyAssociationView(request):
    
    user = Profile.objects.get(user_p = request.user)
    myassocs = association_member.objects.filter(member = user, member_status ='active' )
    if  'searchmyassociation' in request.session:
        publicassocs = association_member.objects.filter(member = user, member_status ='active' ).filter(Q(name__icontains =request.session['searchmyassociation'])  
        |Q(about_us__icontains =request.session['searchmyassociation']) |Q(what_we_do__icontains =request.session['searchmyassociation']))
                    
        del request.session['searchmyassociation']
        page = request.GET.get('page',1)
        paginator = Paginator(publicassocs,8)
        try:
            allpublicassocs = paginator.page(page)
        except PageNotAnInteger:
            allpublicassocs = paginator.page(1)
        except EmptyPage:
            allpublicassocs= paginator.page(paginator.num_pages)
    else:
        publicassocs = association_member.objects.filter(member = user, member_status ='active' )
        page = request.GET.get('page',1)
        paginator = Paginator(publicassocs,8)
        try:
            allpublicassocs = paginator.page(page)
        except PageNotAnInteger:
            allpublicassocs = paginator.page(1)
        except:    
            allpublicassocs = paginator.page(paginator.num_pages) 
        
    return render(request,'account/community/mycommunities.html',{'myassocs':myassocs,'allpublicassocs':allpublicassocs})
    


    
def JoinAssociationView(request):
    
    message_list = [{
        
        
    }]        
    if request.method == 'POST':
        
        assoc_id = json.loads(request.body)
        print('POST')
        assoc = association.objects.get(pk=assoc_id)
        user = Profile.objects.get(user_p = request.user)
        userexists = association_member.objects.filter(member =user, myassociation = assoc)
        if userexists.exists():
            message_list = [{
            'message':'You are already a member',
            
            }]  
        else:
            myassoc = association_member(member = user,myassociation = assoc,active_status = 'inactive') 
                   
            myassoc.save()
            message_list = [{
            'message':'success',
            
            }]  
       
    return JsonResponse(message_list,safe=False)   



#add member
@login_required(login_url = 'login')  
def AddMemberGroup(request):
    #assign RegisterForm to variable
    assoc = association.objects.get(pk = request.session['activegroupbackend'])
    form = AddMemberGroupForm()
    
    if request.method == 'POST':
         #pass form for validation
        
        form = AddMemberGroupForm(request.POST)
        #if form is valid and cleaned
        if form.is_valid():
            phone_number = form.cleaned_data['new_member']

            try:
                qs = User.objects.get(phone_number=phone_number)
                member = Profile.objects.get(user_p = qs)
                
                try:
                    members = association_member.objects.get(member = member, myassociation = request.session['activegroupbackend'])
                    if members.member_status != 'active':
                        members.member_status = 'active'
                        members.save()
                        return redirect('members')   
                    else:
                        form.add_error(error = 'User is Already Our Member else an error occured',field =  'new_member')
                        return render (request,'account/form_temp.html',{'form':form})
                   
                    
                except:
                    x = form.save(commit=False)  
                    x.member = member
                    x.active = 'inactive'
                    
                    x.myassociation = assoc
                    x.save()
                    
                    return redirect('members')
            except:
                
            
                form.add_error(error = 'Phone number is not registered',field = 'new_member')
                return render (request,'account/form_temp.html',{'form':form})
      
        else:
            
            return render (request,'account/form_temp.html',{'form':form})
    
  
    return render(request,'account/form_temp.html',{'form':form})   



@login_required(login_url = 'logout')
def ActivategroupView(request):
    user = Profile.objects.get(user_p = request.user)
    message_list = [{       
        
    }]        
    if request.method == 'POST':
        
        group_id = json.loads(request.body)
        try:
    
            assoc = association.objects.get(pk = request.session['activegroup'] )
            assoc.active_status = ['inactive']
            assoc.save()
        
            for key in list(request.session.keys()):
                if not key.startswith("_"): # skip keys set by the django system
                    del request.session[key]
        except:
            pass

        assoc = association_member.objects.get(pk = group_id )
        assoc.active_status = 'active'
        
        request.session['activegroup'] = assoc.pk
        request.session['activegroupbackend'] = assoc.myassociation.pk
        request.session['activefinancialyear'] = assoc.myassociation.financial_year
        assoc.save()
        try:
            financial_year = assoc.myassociation.financial_year
            leader = association_leader.objects.get(financial_year =financial_year,associationleader=assoc,leader_status ='Active' )
                       
            request.session['leaders_role'] = leader.leadership_role
            request.session['position'] = leader.other_position
        except:
            request.session['leaders_role'] = 0
            request.session['position'] = 'Resident'
        message_list = [{
                'message':'success',     
                }]  
       
    return JsonResponse(message_list,safe=False) 





@login_required(login_url = 'logout')
def DeActivategroupView(request):
    user = Profile.objects.get(user_p = request.user)
    message_list = [{       
        
    }]        
    if request.method == 'POST':
        
        group_id = json.loads(request.body)
        try:
    
            assoc = association.objects.get(pk = request.session['activegroup'] )
            assoc.active_status = ['inactive']
            assoc.save()
        
            for key in list(request.session.keys()):
                if not key.startswith("_"): # skip keys set by the django system
                    del request.session[key]
        except:
            pass

        
        
        message_list = [{
                'message':'success',     
                }]  
       
    return JsonResponse(message_list,safe=False) 



#association leaders   
    
def AssociationLeadersView(request):
    
    leaders = association_member.objects.filter(myassociation__pk = request.session['activegroupbackend'])
    search_id = 'leader'
    search_placeholder = 'Search leader to be set'
    return render(request,'account/community/leaders.html',{'search_id':search_id,'search_placeholder':search_placeholder,'leaders':leaders}) 
    

@login_required(login_url = 'login')
def SetLeadersView(request, user_id):
   
    if request.method == 'POST':
         #pass form for validation
        setleader = 'login'
        #assign RegisterForm to variable
        user = Profile.objects.get(user_p__phone_number = user_id)
        assoc = association_member.objects.get(myassociation__pk = request.session['activegroupbackend'], member = user) 
        leader = association_leader.objects.get(financial_year = request.session['activefinancialyear'],associationleader = assoc)
        form = GroupLeaderForm(request.POST, instance = leader)
        #if form is valid and cleaned
        if form.is_valid():
            #if form is submitted with deleted leader_ship status, delete it also.
            #put alert in the front end
            
            leader_status = form.cleaned_data['leader_status']
            if leader_status == 'Deleted':
                leader = association_leader.objects.get(associationleader = assoc,leadership_role = 100,leader_status = 'Deleted')
                leader.delete()
                return redirect('cprofile')
            else:
                if leader.position == 'President':
                    leader.leadership_role = 1 
                    if leader.other_position:
                        pass
                    else:
                        leader.other_position = leader.position                  
                    leader.save()   
                            
                    return redirect('cprofile')
                elif leader.position == 'General Secretary':
                    leader.leadership_role = 2 
                    if leader.other_position:
                        pass
                    else:
                        leader.other_position = leader.position                  
                    leader.save()   
                            
                    return redirect('cprofile')
                    
                elif leader.position == 'Treasurer':
                    leader.leadership_role = 3 
                    if leader.other_position:
                        pass
                    else:
                        leader.other_position = leader.position                  
                    leader.save()   
                            
                    return redirect('cprofile')   

                elif leader.position == 'Other Position':
                    leader.leadership_role = 4 
                    if leader.other_position:
                        pass
                    else:
                        leader.other_position = leader.position                  
                    leader.save()   
                            
                    return redirect('cprofile') 
                    
                    
      
        else:
            
            return render (request,'account/form_temp.html',{'form':form,'setleader':setleader}) 
    else:
        setleader = 'login'
        #assign RegisterForm to variable
        user = Profile.objects.get(user_p__phone_number = user_id)
        assoc = association_member.objects.get(myassociation__pk = request.session['activegroupbackend'], member = user)
        try:
            leader = association_leader.objects.get(financial_year = request.session['activefinancialyear'],associationleader = assoc)

        except:
            leader = association_leader(associationleader = assoc,financial_year = request.session['activefinancialyear'],leadership_role = 100,leader_status = 'Deleted' )
            leader.save()
    form = GroupLeaderForm(instance = leader)
    
    return render (request,'account/form_temp.html',{'form':form,'setleader':setleader})    
            
@login_required(login_url = 'logout')    
def SearchMembersView(request):
   
    if request.method == 'POST':
       
       messagess = json.loads(request.body)
       request.session['searchmember'] = messagess
   
    message_list = [{
      
        'message':'success',
      
    }]
   
    return JsonResponse(message_list,safe=False)     
@login_required(login_url = 'logout')               
def MembersView(request):
    

    if 'activegroupbackend' in request.session:
        members_no = association_member.objects.filter(Q(myassociation__pk = request.session['activegroupbackend']), Q(member_status= 'active')).count()
        if  'searchmember' in request.session:
            members = association_member.objects.filter(Q(
            myassociation__pk = request.session['activegroupbackend']), Q(member_status= 'active')).filter(
             Q(member__user_p__user_name__icontains = request.session['searchmember']) |Q(member__full_name__icontains = request.session['searchmember']) ).order_by('id')
            del request.session['searchmember']
            page = request.GET.get('page',1)
            paginator = Paginator(members,8)
            try:
                allmembers = paginator.page(page)
            except PageNotAnInteger:
                allmembers = paginator.page(1)
            except EmptyPage:
                    allmembers= paginator.page(paginator.num_pages)
        else:
            members = association_member.objects.filter(Q(
           myassociation__pk = request.session['activegroupbackend']), Q(member_status= 'active'))
            page = request.GET.get('page',1)
            paginator = Paginator(members,8)
            try:
                allmembers = paginator.page(page)
            except PageNotAnInteger:
                allmembers = paginator.page(1)
            except EmptyPage:
                    allmembers= paginator.page(paginator.num_pages) 
    else:
        return redirect('logout')
        
    return render(request,'account/community/members.html',{'allmembers':allmembers,'members_no':members_no}) 


@login_required(login_url = 'logout')    
def MemberView(request):
   
    if request.method == 'POST':
       
        messagess = json.loads(request.body)
        request.session['member'] = messagess
   
        message_list = [{
      
        'message':'success',
      
        }]
    else:
        if  'member' in request.session:
            member = Profile.objects.get(pk =request.session['member'])
            projects = Projects.objects.filter(project_owner = member)
            return render(request,'account/profile/viewprofile.html',{'projects':projects,'member':member}) 
        else:
            return redirect('logout')
            
   
    return JsonResponse(message_list,safe=False)





def RemoveMembersView(request,):
    
    message_list = [{
      
    }]        
    if request.method == 'POST':
        
        user_deleted = json.loads(request.body)
        if 'user_removed' in request.session:
            del request.session['user_removed']
        request.session['user_removed'] = user_deleted
        
         
        
        message_list = [{
            'message':'success',
            
            }]  
       
    return JsonResponse(message_list,safe=False)                 
    
def RemoveMembersConfirmView(request):
    member = association_member.objects.get(pk = request.session['user_removed'])
    if request.method == 'POST':
        member.member_status = 'Inactive'
        member.active_status = 'Inactive'
        member.save()
        if 'user_removed' in request.session:
            del request.session['user_removed']
        return redirect('members')
    return render(request,'account/community/confirm.html',{'member':member})

@login_required(login_url = 'logout')    
def SearchInnerAssociationView(request):
   
    if request.method == 'POST':
       
       messagess = json.loads(request.body)
       request.session['searchinnerassociation'] = messagess
   
    message_list = [{
      
        'message':'success',
      
    }]
   
    return JsonResponse(message_list,safe=False)     
    
    
@login_required(login_url = 'logout')       
def InnerAssociationView(request):
    form = GroupForm()
    
    if 'activegroupbackend' in request.session:
        user = Profile.objects.get(user_p = request.user)
        myassocs = association_member.objects.filter(member = user, member_status ='active' )
        members_no = association_member.objects.filter(Q(myassociation__pk = request.session['activegroupbackend']), Q(member_status= 'active')).count()
        innercomms = association.objects.filter(parent = request.session['activegroupbackend'])
        if  'searchinnerassociation' in request.session:
            innercomms = association.objects.filter(Q(parent = request.session['activegroupbackend'])).filter(Q(name__icontains =request.session['searchinnerassociation'])  
            |Q(slogan__icontains =request.session['searchinnerassociation']) |Q(address__icontains =request.session['searchinnerassociation'])
            |Q(about_us__icontains =request.session['searchinnerassociation']) |Q(what_we_do__icontains =request.session['searchinnerassociation'])).order_by('-id')
            
            del request.session['searchinnerassociation']
            page = request.GET.get('page',1)
            paginator = Paginator(innercomms,8)
            try:
                allinnercomms = paginator.page(page)
            except PageNotAnInteger:
                allinnercomms = paginator.page(1)
            except EmptyPage:
                allinnercomms= paginator.page(paginator.num_pages)
        else:
            innercomms = association.objects.filter(Q(parent = request.session['activegroupbackend'])).order_by('-id')
            page = request.GET.get('page',1)
            paginator = Paginator(innercomms,8)
            try:
                allinnercomms = paginator.page(page)
            except PageNotAnInteger:
                allinnercomms = paginator.page(1)
            except EmptyPage:
                allinnercomms = paginator.page(paginator.num_pages) 
    else:
        return redirect('logout')
    
    
    if request.method == 'POST':
         #pass form for validation
        
        form = GroupForm(request.POST)
        #if form is valid and cleaned
        if form.is_valid():
        #save form, login user and redirect user to profile page
            financial_year = form.cleaned_data.get('financial_year')
            user = Profile.objects.get(user_p = request.user)
            try:
                active_assoc = association_member.objects.get(member = user, active_status = 'active')
                active_assoc.active_status = 'inactive'
                active_assoc.save()
            except:
                pass
            assoc = form.save(commit=False)  
            assoc.founder = user
            assoc.parent = request.session['activegroupbackend']
            assoc.approved = 2
            assoc.save()           
            myassoc = association_member(member = user,myassociation = assoc) 
            
            myassoc.save()
            
            request.session['activegroup'] = myassoc.pk
            request.session['activegroupbackend'] = myassoc.myassociation.pk
            request.session['activefinancialyear'] = myassoc.myassociation.financial_year
            
            myassoc_leader  = association_leader(
            associationleader = myassoc,  financial_year = financial_year
            )
            myassoc_leader.save()           
            
            return redirect('cprofile')
    return render(request,'account/community/mychildcommunities.html',{'members_no':members_no,'myassocs':myassocs,'form':form,'allinnercomms':allinnercomms})
    
def RemoveAssocView(request,):
    
    message_list = [{
        
        
    }]        
    if request.method == 'POST':
        
        assoc_deleted = json.loads(request.body)
        if 'assoc_removed' in request.session:
            del request.session['assoc_removed']
        request.session['assoc_removed'] = assoc_deleted
        
         
        
        message_list = [{
            'message':'success',
            
            }]  
       
    return JsonResponse(message_list,safe=False)  
    
def RemoveAssocConfirmView(request):
    assoc = association.objects.get(pk = request.session['assoc_removed'])
    if request.method == 'POST':
        assoc.delete()
        if 'assoc_removed' in request.session:
            del request.session['assoc_removed']
        return redirect('innercommunities')
    return render(request,'account/community/confirm.html',{'assoc':assoc})    
    
def ApproveAssocView(request):
    message_list = [{
        
        
    }]        
    if request.method == 'POST':
        
        assoc = json.loads(request.body)
        assoc = association.objects.get(pk = assoc)
        assoc.approved = 1
        assoc.save()
        
         
        
        message_list = [{
            'message':'success',
            
            }] 
    return JsonResponse(message_list,safe=False)          
    
def DisapproveAssocView(request):
    message_list = [{
        
        
    }]        
    if request.method == 'POST':
        
        assoc = json.loads(request.body)
        assoc = association.objects.get(pk = assoc)
        assoc.approved = 3
        assoc.save()
        
         
        
        message_list = [{
            'message':'success',
            
            }] 
    return JsonResponse(message_list,safe=False)              
    

    