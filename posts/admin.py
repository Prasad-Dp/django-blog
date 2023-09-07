from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Post)
admin.site.register(models.UserProfile)
admin.site.register(models.Followers)
admin.site.register(models.Likes)
admin.site.register(models.Comments)
admin.site.register(models.ReplyComments)