from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from hotel.models import Category
from home.models import Setting
from .models import UserProfile, UserProfileForm
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


@login_required(login_url='/')
def index(request):
    setting = Setting.objects.first()
    category = Category.objects.all()
    profile = UserProfile.objects.get(id=request.user.id)
    context = {
        'setting': setting,
        'category': category,
        'profile': profile,
        'page': "User Profile"
    }
    return render(request, 'user_profile.html', context)


def update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(
            request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():

            user_form.save()
            profile_form.save()
            print("Hata Kontorl  - 2")
            messages.success(request, 'Your account has been updated!')
            return redirect('/user')
        else:
            messages.warning(request, 'Check Form!')
            return redirect('/user/update')
    else:
        setting = Setting.objects.first()
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.userprofile)
        context = {
            'setting': setting,
            'category': category,
            'user_form': user_form,
            'profile_form': profile_form,
            'page': "Update Profile"
        }
        return render(request, 'user_update.html', context)


def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(
                request, 'Your password was successfully updated!')
            return HttpResponseRedirect('/user')
        else:
            messages.warning(
                request, 'Please correct the error below!<br>'+str(form.errors))
            return HttpResponseRedirect('/user/password')
    else:
        category = Category.objects.all()
        form = PasswordChangeForm(request.user)
        return render(request, 'change_password.html', {'form': form, 'category': category, 'page': 'Change Password'})
