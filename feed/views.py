from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.contrib import messages
from django.http import JsonResponse
from .forms import PostForm,EditPostForm
from .models import Posts,Comments,CommentReply,LikedPost,LikedComment
from account.models import Profile
from community.models import association
from django.views.decorators.csrf import csrf_exempt
from django.contrib.humanize.templatetags.humanize import naturaltime

from django.db.models import Q
import json




@login_required(login_url = 'logout')    
def SearchPostsView(request):
   
    if request.method == 'POST':
       
       messagess = json.loads(request.body)
       request.session['searchpost'] = messagess
   
    message_list = [{
      
        'message':'success',
      
    }]
   
    return JsonResponse(message_list,safe=False) 


@login_required(login_url = 'logout')  
def PostsView(request):
    
    if 'activegroupbackend' in request.session:
        current_user = get_object_or_404(Profile,user_p = request.user)
        likeposts = LikedPost.objects.filter(liked_by = current_user,post_liked__posted_to__pk = request.session['activegroupbackend'])
    
    
        if  'searchpost' in request.session:
            
            allposts = Posts.objects.filter(Q(posted_to =request.session['activegroupbackend']) ).filter(Q(post__icontains = request.session['searchpost'])).order_by('-id')
            del request.session['searchpost']
            page = request.GET.get('page',1)
            paginator = Paginator(allposts,2)
            try:
                posts = paginator.page(page)
            except PageNotAnInteger:
                posts = paginator.page(1)
            except EmptyPage:
                posts = paginator.page(paginator.num_pages)
        else:
            allposts = Posts.objects.filter(Q(posted_to =request.session['activegroupbackend']) ).order_by('-id')
            page = request.GET.get('page',1)
            paginator = Paginator(allposts,2)
            try:
                posts = paginator.page(page)
            except PageNotAnInteger:
                posts = paginator.page(1)
            except EmptyPage:
                posts = paginator.page(paginator.num_pages) 
    else:
        return redirect('logout')
    
    return render(request,'account/feed/posts.html',{'likeposts':likeposts,'posts':posts})
 



#CREATE POST  
def CreatePostView(request):
    form = PostForm()
    
    if request.method == 'POST':
         #pass form for validation
        
        form = PostForm(request.POST,request.FILES)
        #if form is valid and cleaned
        if form.is_valid():
            user = Profile.objects.get(user_p = request.user)
            assoc = association.objects.get(pk = request.session['activegroupbackend'])
            post = form.cleaned_data['post']
            if request.FILES.getlist('post_images'):
                images = request.FILES.getlist('post_images')
                if len(images)  >=3:
                    image1 = images[0]
                    image2 = images[1]
                    image3 = images[2]
                    post =  Posts(images = 3,post_image1 = image1,post_image2=image2, post_image3 = image3,posted_by = user ,posted_to =assoc ,post= post) 
                    post.save()
                    return redirect('posts')
                elif len(images) == 2:
                    image1 = images[0]
                    image2 = images[1]
                    post =  Posts(images = 2,post_image1 = image1,post_image2=image2,posted_by = user ,posted_to =assoc ,post= post) 
                    post.save()
                    return redirect('posts')
                elif len(images) == 1:
                    image1 = images[0]
                    post =  Posts(images = 1,post_image1 = image1,posted_by = user ,posted_to =assoc ,post= post) 
                    post.save()
                    return redirect('posts')
            else:    
                post =  Posts(posted_by = user ,posted_to =assoc ,post= post) 
                post.save()
                return redirect('posts')
            
        else:
           
            return render(request,'account/feed/createpost.html',{'form':form}) 
        
        
    return render(request,'account/feed/createpost.html',{'form':form}) 
    
#EDIT POST
def EditPostView(request,post_id):
    post = Posts.objects.get(pk=post_id)
    form = EditPostForm(instance = post)
    
    if request.method == 'POST':
        #pass form for validation
        
        form = EditPostForm(request.POST,request.FILES,instance = post)
        #if form is valid and cleaned
        if form.is_valid():
            
            post.save()
            if 'view_post' in request.session:
                del request.session['view_post']
            request.session['view_post'] = post_id
            return redirect('singlepost')
            
        else:
           
            return render(request,'account/feed/editpost.html',{'form':form}) 
        
        
    return render(request,'account/feed/editpost.html',{'form':form}) 
    
def DeletePostView(request,post_id):
    
    post = Posts.objects.get(pk = post_id)
    post.delete()
    return redirect('posts')


def AjaxSinglePostView(request,):
    
    message_list = [{
        
        
    }]        
    if request.method == 'POST':
        
        post_id = json.loads(request.body)
        if 'view_post' in request.session:
            del request.session['view_post']
        request.session['view_post'] = post_id
        
         
        
        message_list = [{
            'message':'success',
            
            }]  
       
    return JsonResponse(message_list,safe=False) 
    
@login_required(login_url = 'logout')    
def SearchCommentView(request):
   
    if request.method == 'POST':
       
       messagess = json.loads(request.body)
       request.session['searchcomment'] = messagess
   
    message_list = [{
      
        'message':'success',
      
    }]
   
    return JsonResponse(message_list,safe=False) 

    
def SinglePostView(request):
  
    if 'activegroupbackend' in request.session:
        current_user = get_object_or_404(Profile,user_p = request.user)
        post = Posts.objects.get(pk = request.session['view_post'])
    
    
        LikedComments = LikedComment.objects.filter(comment_liked_by = current_user,comment_liked__post_id__pk =request.session['view_post'] )
    
        try:
            liked = LikedPost.objects.get(liked_by = current_user,post_liked=post)
        except:
            liked = []
        
    
        if  'searchcomment' in request.session:
            
            allcomments = Comments.objects.filter(Q(post_id = post)).filter(Q(comment_by__full_name__icontains =request.session['searchcomment'])|
            Q(comment_by__user_p__user_name__icontains =request.session['searchcomment'])|Q(comment__icontains =request.session['searchcomment'] )).order_by('-id')
            del request.session['searchcomment']
            page = request.GET.get('page',1)
            paginator = Paginator(allcomments,2)
            try:
                comments = paginator.page(page)
            except PageNotAnInteger:
                comments = paginator.page(1)
            except EmptyPage:
                comments = paginator.page(paginator.num_pages)
        else:
            allcomments = Comments.objects.filter(Q(post_id = post)).order_by('-id')
            page = request.GET.get('page',1)
            paginator = Paginator(allcomments,2)
            try:
                comments = paginator.page(page)
            except PageNotAnInteger:
                comments = paginator.page(1)
            except EmptyPage:
                comments = paginator.page(paginator.num_pages) 
    else:
        return redirect('logout')    
        
        
        
    return render(request,'account/feed/singlepost.html',{'LikedComments':LikedComments,'post':post,'comments':comments,'liked':liked}) 



   
    
#display all comments, onclick reply fetch that comment and display it alone    
    
    #COMMENTS #
def AjaxCommentView(request):
    current_user = get_object_or_404(Profile,user_p = request.user)
    post_pk = request.session['view_post']
    if request.method == 'POST':
        message = json.loads(request.body)
        post = Posts.objects.get(pk = post_pk)
        post.comment_count += 1
        post.save()
        
        m = Comments.objects.create(comment_by =  current_user,post_id = post,comment = message)
       
        
    
    messages = Comments.objects.filter(post_id = post).order_by('-id')
   
   
    
    message_list = [{
        'comment_by':comment.comment_by.user_p.user_name,
        #comment_by image here
        'comment':comment.comment,
        'date_commented':naturaltime(comment.date_commented),
        'comment_likes_count':comment.comment_likes_count,
        'reply_count':comment.reply_count,
        'comment_id':comment.id,
       
    }for comment in messages]
   
    return JsonResponse(message_list,safe=False) 
    
    
def FetchAjaxCommentView(request):
    
    
    messages = Comments.objects.filter(post_id = post).order_by('-id')
    
    
    message_list = [{
        'comment_by':comment.comment_by.user_p.user_name,
        #comment_by image here
        'comment':comment.comment,
        'date_commented':naturaltime(comment.date_commented),
        'comment_likes_count':comment.comment_likes_count,
        'reply_count':comment.reply_count,
        'comment_id':comment.pk,
        
    }for comment in messages]
    
    return JsonResponse(message_list,safe=False)     
       
def DeleteCommentView(request):
    if request.method == 'POST':
        comment_id = json.loads(request.body)
        comment = Comments.objects.get(pk = comment_id)
        post_id = comment.post_id.pk
        post = Posts.objects.get(pk = post_id)
        post.comment_count -=1
        post.save()
        comment.delete()
    message_list = [{
       
        'message':'success',
    }]
    
    return JsonResponse(message_list,safe=False)         
       

#fecth reply_count
def AjaxReplyView(request):
    current_user = get_object_or_404(Profile,user_p = request.user)
    comment_pk = request.session['view_comment']
    if request.method == 'POST':
        message = json.loads(request.body)
        comment = Comments.objects.get(pk = comment_pk)
        comment.reply_count +=1
        comment.save()
        m = CommentReply.objects.create(reply_by =  current_user,comment_id = comment,reply = message)
       
        
    
    messages = CommentReply.objects.filter(comment_id = comment_pk).order_by('-id')
    
    
    message_list = [{
        'reply_by':comment.reply_by.user_p.user_name,
        #comment_by image here
        'reply':comment.reply,
        'date_replied':naturaltime(comment.date_replied),
       
        'reply_id':comment.id,
       
    }for comment in messages]
    
    return JsonResponse(message_list,safe=False)

    
def AjaxSingleCommentView(request,):
    
    message_list = [{
        
        
    }]        
    if request.method == 'POST':
        
        post_id = json.loads(request.body)
        if 'view_comment' in request.session:
            del request.session['view_comment']
        request.session['view_comment'] = post_id
        
         
        
        message_list = [{
            'message':'success',
            
            }]  
       
    return JsonResponse(message_list,safe=False) 
@login_required(login_url = 'logout')    
def SearchReplyView(request):
   
    if request.method == 'POST':
       
       messagess = json.loads(request.body)
       request.session['searchreply'] = messagess
   
    message_list = [{
      
        'message':'success',
      
    }]
   
    return JsonResponse(message_list,safe=False) 
@login_required(login_url = 'logout')    
def SingleCommentView(request):
    post = Posts.objects.get(pk = request.session['view_post'])
    comment = Comments.objects.get(pk = request.session['view_comment'])
    
    if  'searchreply' in request.session:
            
        reply = CommentReply.objects.filter(Q(comment_id__pk = request.session['view_comment'])).filter(
            Q(reply_by__full_name__icontains =request.session['searchreply'])|
            Q(reply_by__user_p__user_name__icontains =request.session['searchreply'])|
            Q(reply__icontains =request.session['searchreply'] )).order_by('-id')
        del request.session['searchreply']
        page = request.GET.get('page',1)
        paginator = Paginator(reply,2)
        try:
            replys = paginator.page(page)
        except PageNotAnInteger:
            replys = paginator.page(1)
        except EmptyPage:
            replys = paginator.page(paginator.num_pages)
    else:
        reply = CommentReply.objects.filter(Q(comment_id__pk = request.session['view_comment']))
        page = request.GET.get('page',1)
        paginator = Paginator(reply,2)
        try:
            replys = paginator.page(page)
        except PageNotAnInteger:
            replys = paginator.page(1)
        except EmptyPage:
            replys = paginator.page(paginator.num_pages) 
    return render(request,'account/feed/replycomment.html',{'post':post,'comment':comment,'replys':replys})     
    
    
def AjaxlikePostView(request,):
    current_user = get_object_or_404(Profile,user_p = request.user)
    message_list = [{
        
        
    }]        
    if request.method == 'POST':
        
        post_id = json.loads(request.body)
        post = Posts.objects.get(pk = post_id)
        try:
           
            liked = LikedPost.objects.get(liked_by = current_user,post_liked=post)
            liked.delete()
            post.likes_count -=1
            count = post.likes_count
            post.save()
            
        except:
            post.likes_count +=1
            count = post.likes_count
            post.save()
            likepost = LikedPost.objects.create(liked_by = current_user,post_liked=post)
        
         
        
        message_list = [{
            'message':'success',
            'count':count,
            
            }]  
       
    return JsonResponse(message_list,safe=False)     
    
    
def AjaxlikeCommentView(request,):
    current_user = get_object_or_404(Profile,user_p = request.user)
    message_list = [{
        
        
    }]        
    if request.method == 'POST':
        
        comment_id = json.loads(request.body)
        comment = Comments.objects.get(pk = comment_id)
        try:
           
            liked = LikedComment.objects.get(comment_liked_by = current_user,comment_liked=comment)
            liked.delete()
            comment.comment_likes_count -=1
            count = comment.comment_likes_count
            comment.save()
            
        except:
            comment.comment_likes_count +=1
            count = comment.comment_likes_count
            comment.save()
            likecomment = LikedComment.objects.create(comment_liked_by = current_user,comment_liked=comment)
        
         
        
        message_list = [{
            'message':'success',
            'count':count,
            
            }]  
       
    return JsonResponse(message_list,safe=False) 

#DELETE REPLY    
def DeleteReplyView(request):
    if request.method == 'POST':
        reply_id = json.loads(request.body)
        reply = CommentReply.objects.get(pk = reply_id)
        comment_id = reply.comment_id.pk
        comment = Comments.objects.get(pk = comment_id)
        comment.reply_count -=1
        comment.save()
        reply.delete()
    message_list = [{
       
        'message':'success',
    }]
    
    return JsonResponse(message_list,safe=False)         
           