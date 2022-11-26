from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime

class User(AbstractUser):
    pass

class Post(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="posts")
    post=models.CharField(max_length=200,null=True)
    time=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return(f"Post {self.id} by {self.user} at [{self.time}]")


class Like(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name="likes")

class Comment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    comment=models.CharField(max_length=200,null=True)

class Follower(models.Model):
    follow=models.ForeignKey(User,on_delete=models.CASCADE,related_name="followers")
    followers=models.ManyToManyField(User,blank=True,related_name='following')