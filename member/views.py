#MEMBER MEMBER MEMBER
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import Profile
from django.contrib.auth.decorators import login_required
# Create your views here.

def signup(request):
    page = 'signup'

    #receive user credentials
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')

        if password == password1:
            if User.objects.filter(username=username).exists():
                messages.info(request, "username '{}' is taken".format(username))
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "email '{}' is taken".format(email))
                return redirect('signup')
            else:
                user = User.objects.create_user(
                username = username,
                email = email,
                )
                user.set_password(password)
                user.save()

                # CREATE A PROFILE OBJECT FOR THE SIGNED UP USER
                user_profile = Profile.objects.create(
                user = user
                )
                user_profile.save()

                return redirect('login')
        else:
            messages.info(request, 'Password do not match')
            return redirect('signup')

    context = {
    'page':page
    }
    return render(request, 'signup_login.html', context)

def login(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password = password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.warning(request, 'Please enter the correct credentials')
            return redirect('login')

    context = {
    'page':page
    }
    return render(request, 'signup_login.html', context)

def logout(request):
    auth.logout(request)
    return redirect('login')

login_required(login_url='login')
def settings(request):
    user = User.objects.get(id=request.user.id)
    user_profile = Profile.objects.get(user=user)

    if request.method == 'POST':
        avatar = request.FILES.get('avatar')
        username = request.POST.get('username')
        name = request.POST.get('name')
        bio = request.POST.get('bio')
        email = request.POST.get('email')
        location = request.POST.get('location')

        default_avatar = user_profile.avatar

        # CHECK IF THE AVATAR IS EMPTY
        if avatar == None:
            user_profile.avatar = default_avatar
            user.username = username
            user_profile.name = name
            user_profile.bio = bio
            user.email = email
            user_profile.location = location
            user.save()
            user_profile.save()
            return redirect('settings')
        else:
            user_profile.avatar = avatar
            user.username = username
            user_profile.name = name
            user_profile.bio = bio
            user.email = email
            user_profile.location = location
            user.save()
            user_profile.save()

            return redirect('settings')

    context = {
    'user':user,
    'user_profile':user_profile
    }
    return render(request, 'settings.html', context)

# login_required(login_url='login')
# def change_password(request):
#     user = User.objects.get(id=request.user.id)
#     old_user_password = user.password
#
#     if request.method == 'POST':
#         password_old = request.POST.get('password_old')
#         password_new = request.POST.get('password_new')
#         password_new1 = request.POST.get('password_new1')
#
#         if old_user_password == password_old:
#             if password_new == password_new1:
#                 user.set_password(password_new)
#                 user.save()
#                 messages.success(request, 'Password changed successfully')
#                 return redirect('settings')
#             else:
#                 messages.warning(request, 'New Password do not match')
#                 return redirect('change_password')
#         else:
#             messages.warning(request, 'Error in current password')
#             return redirect('change_password')
#
#
#     return render(request, 'change_password.html')
