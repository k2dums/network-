from django.contrib import admin

from .models import User,Like,Comment,Follower,Post

class FollowerAdmin(admin.ModelAdmin):
        list_display=("follow","by")
# Register your models here.
admin.site.register(User)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Follower,FollowerAdmin)
admin.site.register(Post)