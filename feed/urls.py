from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('editpost/<post_id>/',views.EditPostView,name ='editpost'),
    path('createpost/',views.CreatePostView,name ='createpost'),
    path('deletepost/<post_id>/',views.DeletePostView,name ='deletepost'),
    path('posts/',views.PostsView,name ='posts'),
    path('searchposts/',views.SearchPostsView,name ='searchposts'),
    path('ajaxsinglepost',views.AjaxSinglePostView,name ='ajaxsinglepost'),
    path('ajaxlikepost',views.AjaxlikePostView,name ='ajaxlikepost'),
    
    path('singlepost',views.SinglePostView,name ='singlepost'),
    
    
    
    
    path('searchcomment',views.SearchCommentView,name ='searchcomment'),
    path('deletecomment',views.DeleteCommentView,name ='deletecomment'),
    path('ajaxcomment',views.AjaxCommentView,name ='ajaxcomment'),
    path('ajaxlikecomment',views.AjaxlikeCommentView,name ='ajaxlikecomment'),
    path('fetchajaxcomment',views.FetchAjaxCommentView,name ='fetchajaxcomment'),
    
    path('searchreply',views.SearchReplyView,name ='searchreply'),
    path('deletereply',views.DeleteReplyView,name ='deletereply'),
    path('ajaxreply',views.AjaxReplyView,name ='ajaxreply'),
    path('ajaxsinglecomment',views.AjaxSingleCommentView,name ='ajaxsinglecomment'),
    path('reply',views.SingleCommentView,name ='reply'),
    ]