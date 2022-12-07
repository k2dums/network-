from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime

class User(AbstractUser):
    
    def serialize(self):
        return {
         "username":self.username,
         "email":self.email,  
        }

class Post(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="posts")
    post=models.CharField(max_length=200,null=True)
    time=models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            'user':self.user.username,
            'post':self.post,
            'time':self.time,
        }
    def __str__(self):
        return(f" Post [{self.id}] created by {self.user} ")


class Like(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='likes')
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name="likes")

    class Meta:
        constraints=[ models.UniqueConstraint(fields=['user','post'],name='unique user likes')]


    def __str__(self):
        return(f'Like_id:[{self.id}]---[{self.post}]liked by {self.user}')

class Comment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    comment=models.CharField(max_length=200,null=True)

    def __str__(self):
        return (f"Comment_id:[{self.id}]---[{self.post}] comment by {self.user}")

class Follower(models.Model):
    follow=models.ForeignKey(User,on_delete=models.CASCADE,related_name="followers")
    by=models.ForeignKey(User,on_delete=models.CASCADE,related_name='following')

    def __str__(self):
        return(f"Follower_id:[{self.id}]---{self.follow} by {self.by}")