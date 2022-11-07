from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Post, Comment, Follow
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from itertools import chain
import random
# Create your views here.

@login_required(login_url='member/login')
def home(request):
    user = request.user.username
    following = Follow.objects.filter(follower=user)#users the current user follow

    # FILTERING POST BY THOSE YOU FOLLOW
    following_accounts = [] # usernames of those current user follows
    posts = [] # list to recieve all posts
    suggested_accounts = [] # list of suggested_accounts

    for i in following:
        following_accounts.append(i.followed)

    # loop through users the current user follows for their posts
    for i in following_accounts:
        new_post = Post.objects.filter(user__username=i)
        posts.append(new_post)

    all_posts = list(chain(*posts)) # chain the posts

    # USER FOLLOW SUGGESTIONS
    accounts_except_user = User.objects.exclude(username=user)# all users except the current logged in user

    for i in accounts_except_user:
        answer = False
        for x in following_accounts:#loop through users we follow
            if i.username == x:
                answer = True

        if answer == False: # if current user doens't follow
            suggested_accounts.append(i)# add to the suggested_accounts

    final_suggested_accounts = suggested_accounts[0:10]#reduce the list to 10 accounts
    random.shuffle(final_suggested_accounts)# shuffle the accounts

    #  WORKING ON LIKED POST
    if request.method == 'POST':
        post_id = request.POST.get('post_id')

        liked_post = Post.objects.get(id=post_id)#receive particular post
        liked_post_members = liked_post.likes.all()#receive all posts

        liked_member = ''

        for i in liked_post_members:# loop through all liked members
            if i.username == user:  #if username of the current loop=current user
                liked_member = i.username #place user in the variable

        if liked_member != '' :
            liked_post.likes.remove(request.user)
        else:
            liked_post.likes.add(request.user)

    context = {
    'all_posts':all_posts,
    'final_suggested_accounts':final_suggested_accounts,
    #'alert':alert
    }
    return render(request, 'home.html',context)

#UPLOADING POST
@login_required(login_url='login')
def upload_post(request):

    user = User.objects.get(id=request.user.id)

    if request.method == 'POST':
        image = request.FILES.get('image')
        caption = request.POST.get('caption')

        if image == None and caption == '':
            messages.warning(request, 'Cannot upload empty post')
            return redirect('upload_post')
        else:
            new_post = Post.objects.create(
            user = user,
            image = image,
            caption = caption
            )
            return redirect('/')

    return render(request, 'upload_post.html')

#VIEWING POST
@login_required(login_url='login')
def view_post(request, pk):

    viewed_post = Post.objects.get(id=pk)
    post_comments = viewed_post.comments.all()

    #WORKING ON THE COMMENT SECTION
    if request.method == 'POST':
        body = request.POST.get('body')

        if body == '':
            return redirect('view_post/'+pk)
        else:
            new_comment = Comment.objects.create(
            user = request.user,
            post = viewed_post,
            body = body
            )
            return redirect('/view-post/'+pk)

    context = {
    'viewed_post':viewed_post,
    'post_comments':post_comments
    }
    return render(request, 'view_post.html', context)

#DELETING POST
@login_required(login_url='login')
def delete_post(request, pk):

    post = Post.objects.get(id=pk)

    if request.method == 'POST':
        post.delete()
        return redirect('/')

    return render(request, 'delete_post.html')

def favorites(request):
    all_posts = Post.objects.filter(favorite=True)

    context = {
    'all_posts':all_posts
    }
    return render(request, 'favorites.html', context)

@login_required(login_url='login')
def add_favorite(request, pk): # pk is the id
    post = Post.objects.get(id=pk)
    post.favorite = True
    post.save()
    return redirect('/')

@login_required(login_url='login')
def remove_favorite(request, pk):
    post = Post.objects.get(id=pk)
    post.favorite = False
    post.save()
    return redirect('/')

@login_required(login_url='login')
def profile(request, pk):
    user = User.objects.get(username=pk)
    posts = Post.objects.filter(user=user)
    num_of_posts = posts.count()
    follower = request.user.username

    #CHECKING THE TOTAL NUMBER OF LIKES
    num_of_likes = 0
    for i in posts:
        num_of_likes += i.likes.count()

    followers = Follow.objects.filter(followed=user.username).count()
    following = Follow.objects.filter(follower=user.username).count()

    if Follow.objects.filter(followed=user.username, follower=follower).first():
        submit_text = "Unfolllow"
    else:
        submit_text = "Follow"

    context = {
    'user':user,
    'posts':posts,
    'num_of_posts':num_of_posts,
    'num_of_likes':num_of_likes,
    'submit_text':submit_text,
    'followers':followers,
    'following':following,
    }
    return render(request, 'profile.html', context)

@login_required(login_url='login')
def follow(request, pk):
    # WORKING WITH THE FOLLOW BUTTON
    if request.method == 'POST':
        followed = request.POST.get('followed')
        follower = request.POST.get('follower')

        follows = Follow.objects.filter(followed=followed, follower=follower).first()

        if follows:
            follows.delete()
            return redirect('profile', pk)
        else:
            new_follower = Follow.objects.create(
            followed = followed,
            follower = follower
            )
            new_follower.save()
            return redirect('profile', pk)

@login_required(login_url='login')
def search_result(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    searched_users = User.objects.filter(username__icontains=q)
    posts = []

    for i in searched_users:
        post = Post.objects.filter(user__username=i.username)
        posts.append(post)

    final_posts = list(chain(*posts))
    new_final_posts = final_posts[0:5]

    context = {
    'searched_users':searched_users,
    'new_final_posts':new_final_posts
    }
    return render(request, 'search_result.html', context)
