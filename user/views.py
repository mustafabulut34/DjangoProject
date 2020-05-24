from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

from hotel.models import Category, Comment
from home.models import Setting
from reservation.models import Reservation
from .models import UserProfile, UserProfileForm

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from .forms import UserUpdateForm


@login_required(login_url='/login')
def index(request):
    setting = Setting.objects.first()
    category = Category.objects.all()
    profile = UserProfile.objects.get(id=request.user.id)
    profile = get_object_or_404(UserProfile, id=request.user.id)
    context = {
        'setting': setting,
        'category': category,
        'profile': profile,
        'page': "User Profile"
    }
    return render(request, 'user_profile.html', context)


@login_required(login_url='/login')
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


@login_required(login_url='/login')
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


@login_required(login_url='/login')
def reservations(request):
    setting = Setting.objects.first()
    category = Category.objects.all()
    reservations = Reservation.objects.filter(user_id=request.user.id)
    context = {
        'setting': setting,
        'category': category,
        'page': 'My Reservations',
        'reservations': reservations
    }
    return render(request, 'user_reservations.html', context)


@login_required(login_url='/login')
def reservation_detail(request, id):
    setting = Setting.objects.first()
    category = Category.objects.all()
    reservation = get_object_or_404(
        Reservation, id=id, user_id=request.user.id)
    context = {
        'setting': setting,
        'category': category,
        'page': 'Reservation Detail',
        'reservation': reservation
    }
    return render(request, 'user_reservation_detail.html', context)


@login_required(login_url='/login')
def comments(request):
    setting = Setting.objects.first()
    category = Category.objects.all()
    comments = Comment.objects.filter(user_id=request.user.id)
    context = {
        'setting': setting,
        'category': category,
        'comments': comments,
        'page': 'My Comments'
    }
    return render(request, 'user_comments.html', context)


@login_required(login_url='/login')
def delete_comment(request, id):
    Comment.objects.get(user_id=request.user.id, id=id).delete()
    messages.success(request, 'Message deleted!')
    return HttpResponseRedirect('/user/comments')
