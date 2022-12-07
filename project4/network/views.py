from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from .models import Post,User,Follower,Like
from django.contrib.auth.decorators import login_required
import json
from django.views.decorators.csrf import csrf_exempt
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

    return render(request, "network/index.html",{"posts":Post.objects.order_by("-time").all()})


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

@csrf_exempt
def profile(request,username):
    if not(request.user.is_authenticated):
        return render (request,'network/login.html',{'message':'Need to be logged in to view the profile'})
    try:
        profile=User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({"Error": "User Profile not found"},status=404) 
    if request.method=="PUT":
        data=json.loads(request.body)
        if data.get("follow") is not None:
            try:
                follower_obj=Follower.objects.get(follow=profile,by=request.user)
                if data.get("follow")==False and follower_obj:
                    follower_obj.delete()
               
            except Follower.DoesNotExist:
                 if data.get("follow")==True:
                    follower_obj=Follower(follow=profile,by=request.user)
                    follower_obj.save()
               
           
    posts=User.objects.get(username=username).posts.order_by("-time").all()
    follow_status=False
    try:
        if (Follower.objects.get(follow=profile,by=request.user)):
            follow_status=True
    except Follower.DoesNotExist:
        pass

    return render(request,"network/profile.html",{"profile":profile,"posts":posts,"follow_status":follow_status})


 

@login_required
def following(request,username):
    following__=request.user.following.all()
    print(following__)
    following__=[following.follow for following in following__]
    posts=Post.objects.order_by("-time").filter(user__in=following__)
    return render(request,"network/following.html",{
        "followings":following__,
        "posts":posts,
        })
@csrf_exempt
@login_required
def post(request,post_id):
    try:
        post__=Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"Error":"Post does not exist"},status=404)
    if request.method == "GET":
        return JsonResponse(post__.serialize())
    if request.method=='PUT':
        try:
            like_obj=Like.objects.filter(post=post__,user=request.user)
            if  like_obj:
                print(f"[Delete] the {like_obj} is being deleted")
                like_obj.delete()
                return JsonResponse({"status":False,"likes":len(post__.likes.all())},status=200)
            else:
                like_obj=Like(user=request.user,post=post__)
                like_obj.save()
                print(f"[Created] the {like_obj} has been deleted")
                return JsonResponse({"status":True,"likes":len(post__.likes.all())},status=201)
        except Like.DoesNotExist:
            return JsonResponse({"status":False},status=201)
    
