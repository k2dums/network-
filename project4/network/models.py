from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="posts")
    img_url=models.CharField(max_length=200,null=True)
    description=models.CharField(max_length=200,null=True)
    hasPhoto=models.BooleanField(default=False)

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