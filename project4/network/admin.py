from django.contrib import admin

from .models import User,Like,Comment,Follower,Post

class PostAdmin(admin.ModelAdmin):
        filter_horizontal=('like',)
class FollowerAdmin(admin.ModelAdmin):
        list_display=("follow","by")
# Register your models here.
class LikeAdmin(admin.ModelAdmin):
        list_display= ('post','user','flag')
admin.site.register(User)
admin.site.register(Like,LikeAdmin)
admin.site.register(Comment)
admin.site.register(Follower,FollowerAdmin)
admin.site.register(Post,PostAdmin)