from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from imagekit.models import ProcessedImageField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from account.models import Profile
from community.models import association

class Posts(models.Model):
    posted_by = models.ForeignKey(Profile,on_delete = models.CASCADE, related_name = 'posted_by')
    posted_to = models.ForeignKey(association,on_delete = models.CASCADE, related_name = 'posted_to')
    post = models.TextField()
    post_image1 = ProcessedImageField(upload_to='media',blank=True, null=True,
                                           
                                           format='JPEG',
                                           options={'quality': 100})
    post_image2 = ProcessedImageField(upload_to='media',blank=True, null=True,
                                           
                                           format='JPEG',
                                           options={'quality': 100})
    post_image3 = ProcessedImageField(upload_to='media',blank=True, null=True,
                                           
                                           format='JPEG',
                                           options={'quality': 100})
    likes_count = models.IntegerField(default = 0)
    comment_count = models.IntegerField(default = 0)
    images = models.IntegerField(default = 0)
    date_posted = models.DateTimeField(auto_now_add = True) 
    
          
    def __str__(self):
        return str(self.posted_by)+'('+str(self.posted_to)+')'
        
        
class Comments(models.Model):
    comment_by = models.ForeignKey(Profile,on_delete = models.CASCADE, related_name = 'comment_by')
    post_id = models.ForeignKey(Posts,on_delete = models.CASCADE, related_name = 'post_id')
    comment = models.TextField()
   
    comment_likes_count = models.IntegerField(default = 0)
    reply_count = models.IntegerField(default = 0)
    
    date_commented = models.DateTimeField(auto_now_add = True) 
    
          
    def __str__(self):
        return self.comment    
        
class CommentReply(models.Model):
    reply_by = models.ForeignKey(Profile,on_delete = models.CASCADE, related_name = 'reply_by')
    comment_id = models.ForeignKey(Comments,on_delete = models.CASCADE, related_name = 'comment_id')
    reply = models.TextField()
   
    date_replied = models.DateTimeField(auto_now_add = True) 
    
          
    def __str__(self):
        return str(self.reply_by)+'('+str(self.reply)+')'      
               
        
        
        
class LikedPost(models.Model):
    liked_by = models.ForeignKey(Profile,on_delete = models.CASCADE, related_name = 'liked_by')
    post_liked = models.ForeignKey(Posts,on_delete = models.CASCADE, related_name = 'post_liked')
    
    date_liked = models.DateTimeField(auto_now_add = True) 
    
          
    def __str__(self):
        return str(self.post_liked)      


class LikedComment(models.Model):
    comment_liked_by = models.ForeignKey(Profile,on_delete = models.CASCADE, related_name = 'comment_liked_by')
    comment_liked = models.ForeignKey(Comments,on_delete = models.CASCADE, related_name = 'comment_liked')  
    date_liked = models.DateTimeField(auto_now_add = True) 
    
          
    def __str__(self):
        return str(self.comment_liked)          