from django.db import models
from django.contrib.auth.models import User
from autoslug import AutoSlugField
from django.db.models.signals import post_save
import uuid
# Create your models here.
class UserProfile(models.Model):
    name=models.CharField(max_length=30)
    pfg_img=models.ImageField(upload_to="pfg_images",null=True, blank=True)
    pbg_img=models.ImageField(upload_to="png_images", null=True, blank=True)
    about=models.TextField()
    location=models.CharField(max_length=20)
    user=models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self) :
        return '%s' % (self.user)


class Post(models.Model):
    tittle=models.CharField(max_length=200)
    post_img=models.ImageField(upload_to="post_images" ,null=True, blank=True)
    post_disc=models.TextField()
    userprofile=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    category=models.CharField(max_length=30)
    time_stamp=models.DateTimeField(auto_now_add=True)
    slug=AutoSlugField(populate_from='tittle' ,unique=True ,blank=True ,primary_key=True)

    def __str__(self):

        return '%s' % (self.tittle)


class Followers(models.Model):
    following=models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name="following")
    follower=models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name="follower") 

class Likes(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    liked_users=models.ForeignKey(UserProfile,on_delete=models.CASCADE)

class Comments(models.Model):
    id=models.UUIDField(primary_key = True,
         default = uuid.uuid4,
         editable = False)
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    comment=models.TextField()
    commenter=models.ForeignKey(UserProfile,on_delete=models.CASCADE)

class ReplyComments(models.Model):
    id=models.UUIDField(primary_key = True,
         default = uuid.uuid4,
         editable = False)
    comment=models.ForeignKey(Comments,on_delete=models.CASCADE)
    replycomment=models.TextField()
    replycommenter=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    

def post_user_created_signel(sender,instance,created,**kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(post_user_created_signel,sender=User)
    
