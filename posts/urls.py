from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name="index"),
    path('login/',views.login_page,name="login"),
    path('signup',views.sign_up,name="signup"),
    path('logout',views.log_out,name="logout"),
    path('home/',views.home,name='home'),
    path('blogpost/',views.BlogPost.as_view(),name="blog-post"),
    path('profile/<str:value>/',views.profile,name="profile"),
    path('home/<slug>/',views.blog_view,name="blog-view"),
    path('profileupdate/<int:pk>',views.profileupdate,name="profile-update"),
    path('posts/<str:category>/',views.post_cat,name='posts'),
    path('latestposts',views.latest_posts,name="latest-posts"),
    path('follow/',views.follow,name="follow"),
    path('likes/',views.post_likes,name="likes"),
    path('comment/',views.post_comments,name="comment"),
    path('replycomments/',views.reply_comment,name="replycomments"),
    
]