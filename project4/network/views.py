from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Post,User
from django.contrib.auth.decorators import login_required


def index(request):
    if request.method=="POST":
        new_post=request.POST.get("new_post")
        if new_post:
            #post_obj is used to refer a newly created object from Post class model
            post_obj=Post()
            user=request.user
            user=User.objects.get(username=user)
            post_obj.user=request.user
            post_obj.post=new_post
            post_obj.save()
            print(f"[SAVED]{post_obj}")
    return render(request, "network/index.html",{"posts":Post.objects.all()})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def profile(request,username):
    user_obj=User.objects.get(username=username)
    post_obj=user_obj.posts.all()
    return render(request,"network/profile.html",{"profile":user_obj,"posts":post_obj,})

@login_required
def following(request,username):
    print(request.user.following.all())
    return render(request,"network/following.html",{"followings":request.user.following.all()})