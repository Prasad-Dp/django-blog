from typing import Any
from django.db import models
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post,UserProfile,Followers,Likes,Comments,ReplyComments
from django.views.generic.edit import CreateView
from .forms import BlogForm,UserProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect("/home")
    
    return render(request,"index.html")

def login_page(request):
    if request.user.is_authenticated:
        return redirect("/home")
    else:
        if request.method=="POST":
            username=request.POST['username']
            password=request.POST['password']
            user=authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect("/home")
            else:
                return redirect("/login")

    return render(request,"authentication/login.html")

def sign_up(request):
    if request.user.is_authenticated:
        return redirect("/home")
    else:
        if request.method=="POST":
            username=request.POST['username']
            email=request.POST['email']
            password1=request.POST['password1']
            password2=request.POST['password2']
            if password1==password2:
                if User.objects.filter(username=username).exists():
                    messages.info(request,"Username Exisist")
                    return redirect("/signup")
                elif User.objects.filter(email=email).exists():
                    messages.info(request,"Email Already Exists")
                    return redirect("/signup")
                else:
                    User.objects.create_user(username=username,email=email,password=password2,)

                    user=authenticate(request,username=username,password=password1)
                    login(request,user)
                    return redirect("/home")
                    
            else:
                messages.info(request,"Password not maching")
                return redirect("/signup")

            
    return render(request,"authentication/signup.html")

def log_out(request):
    logout(request)
    return redirect("/login")

@login_required(login_url="/login")
def home(request):
    posts=Post.objects.all().order_by('-time_stamp')
    lposts=Post.objects.all().order_by('-time_stamp')[ :3]
    eposts=Post.objects.filter(category='Entertainment').order_by('-time_stamp')[ :3]
    sposts=Post.objects.filter(category='Sports').order_by('-time_stamp')[ :3]
    nposts=Post.objects.filter(category='News').order_by('-time_stamp')[ :3]
    print(eposts)
    context={
        'posts':posts,
        'lposts':lposts,
        'eposts':eposts,
        'sposts':sposts,
        'nposts':nposts,
        'ncat':'News',
        'ecat':'Entertainment',
        'scat':'Sports'
    }
    return render(request,"posts/blog-home.html",context)

@login_required(login_url="/login")
def blog_view(request,slug):
    post=Post.objects.get(slug=slug)
    likes_count=Likes.objects.filter(post=Post.objects.get(slug=slug)).count()
    comments=Comments.objects.filter(post=Post.objects.get(slug=slug))
    replys=ReplyComments.objects.all()

    if Likes.objects.filter(post=Post.objects.get(slug=slug),liked_users=UserProfile.objects.get(user=User.objects.get(username=request.user.username))):
        button_txt="Unlike"
    else:
        button_txt="Like"

    context={
        'post':post,
        'likes_count':likes_count,
        'button_txt':button_txt,
        'comments':comments,
        'replys':replys
    }
    return render(request,"posts/blog-details.html",context)

@login_required
def profile(request,value):
    profile_info=UserProfile.objects.get(user=User.objects.get(username=value))
    posts=Post.objects.filter(userprofile=UserProfile.objects.get(user=User.objects.get(username=value)))
    posts_count=Post.objects.filter(userprofile=UserProfile.objects.get(user=User.objects.get(username=value))).count()
    Followers_count=Followers.objects.filter(following=UserProfile.objects.get(user=User.objects.get(username=value))).count()
    followers_list=Followers.objects.filter(following=UserProfile.objects.get(user=User.objects.get(username=value)))
    following_count=Followers.objects.filter(follower=UserProfile.objects.get(user=User.objects.get(username=value))).count()
    following_list=Followers.objects.filter(follower=UserProfile.objects.get(user=User.objects.get(username=value)))
    
    if Followers.objects.filter(following=UserProfile.objects.get(user=User.objects.get(username=value)),follower=UserProfile.objects.get(user=User.objects.get(username=request.user.username))):
        button_text="Unfollow"
    else:
        button_text="Follow"
    context={
        'profile':profile_info,
        'posts':posts,
        'posts_count':posts_count,
        'followers_count':Followers_count,
        'followers_list':followers_list,
        'button_text':button_text,
        'following_count':following_count,
        'following_list':following_list,
    }
    return render(request,"profile/profile.html",context)



class BlogPost(LoginRequiredMixin ,CreateView):
    template_name="posts/blog-post.html"
    form_class=BlogForm

    def form_valid(self, form):
        post = form.save(commit=False)
        print(post)
        post.userprofile=UserProfile.objects.get(user=self.request.user)
        # I do other stuff here
        post.save()

        return redirect("/home")
    
def profileupdate(request,pk):
    data=UserProfile.objects.get(user=pk)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES,instance=data)

        if form.is_valid():
            form.save()
            return redirect('/home')
    else:
        form = UserProfileForm(instance=data)
    return render(request, 'profile/profile_update.html', {'form': form})

def post_cat(request,category):
    posts=Post.objects.filter(category=category).order_by('-time_stamp')
    context={
        'posts':posts
    }
    return render(request,"posts/blog-category.html",context)

def latest_posts(request):
    posts=Post.objects.all().order_by('-time_stamp')
    context={
        'posts':posts
    }
    return render(request,"posts/latest_posts.html",context)

def follow(request):
    if request.method=="POST":
        follow=request.POST['user']
        following=UserProfile.objects.get(user=User.objects.get(username=follow))
        follower=UserProfile.objects.get(user=User.objects.get(username=request.user.username))

        if Followers.objects.filter(following=following,follower=follower).first():
            delete_follower=Followers.objects.get(following=following,follower=follower)
            delete_follower.delete()
            return redirect('/profile/'+follow)
        else:
            new_follower=Followers.objects.create(following=following,follower=follower)
            new_follower.save()
            return redirect('/profile/'+follow)
    else:

        return redirect("/")
    

def post_likes(request):
    if request.method=="POST":
        post_name=request.POST['post']
        post=Post.objects.get(slug=post_name)
        liked_user=UserProfile.objects.get(user=User.objects.get(username=request.user.username))
        if Likes.objects.filter(post=post,liked_users=liked_user).first():
            delete_like=Likes.objects.get(post=post,liked_users=liked_user)
            delete_like.delete()
            return redirect('/home/'+post_name)
        else:
            new_like=Likes.objects.create(post=post,liked_users=liked_user)
            new_like.save()
            return redirect('/home/'+post_name)

    else:
        return redirect("/")
    
def post_comments(request):
    if request.method=="POST":
        post_name=request.POST['post']
        post=Post.objects.get(slug=post_name)
        comment=request.POST['comment']
        commenter=UserProfile.objects.get(user=User.objects.get(username=request.user.username))
        comment_obj=Comments.objects.create(post=post,comment=comment,commenter=commenter)
        comment_obj.save()
        return redirect('/home/'+post_name)

    else:
        return render('/')
    

def reply_comment(request):
    if request.method=="POST":
        post=request.POST['post']
        comment_name=request.POST['comment']
        print(comment_name)
        comments=Comments.objects.get(id=comment_name)
        reply=request.POST['reply']
        print(reply)
        replycommenter=UserProfile.objects.get(user=User.objects.get(username=request.user.username))
        reply_obj=ReplyComments.objects.create(comment=comments,replycomment=reply,replycommenter=replycommenter)
        reply_obj.save()
        return redirect('/home/'+post)