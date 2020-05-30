from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

from hotel.models import Category, Comment
from home.models import Setting
from content.models import Menu, Content, ContentForm, CImagesForm, CImages
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
    category = Category.objects.filter(status=True)
    menu = Menu.objects.filter(status=True)
    profile = get_object_or_404(UserProfile, user_id=request.user.id)
    context = {
        'setting': setting,
        'category': category,
        'menu': menu,
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
            messages.success(request, 'Your account has been updated!')
            return redirect('/user')
        else:
            messages.warning(request, 'Check Form!')
            return redirect('/user/update')
    else:
        setting = Setting.objects.first()
        menu = Menu.objects.filter(status=True)
        category = Category.objects.filter(status=True)
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.userprofile)
        context = {
            'setting': setting,
            'category': category,
            'menu': menu,
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
        category = Category.objects.filter(status=True)
        menu = Menu.objects.filter(status=True)
        form = PasswordChangeForm(request.user)
        return render(request, 'change_password.html', {'form': form, 'category': category, 'menu': menu, 'page': 'Change Password'})


@login_required(login_url='/login')
def reservations(request):
    setting = Setting.objects.first()
    category = Category.objects.filter(status=True)
    menu = Menu.objects.filter(status=True)
    reservations = Reservation.objects.filter(
        user_id=request.user.id).order_by('-created_at')
    context = {
        'setting': setting,
        'category': category,
        'menu': menu,
        'page': 'My Reservations',
        'reservations': reservations
    }
    return render(request, 'user_reservations.html', context)


@login_required(login_url='/login')
def reservation_detail(request, id):
    setting = Setting.objects.first()
    category = Category.objects.filter(status=True)
    menu = Menu.objects.filter(status=True)
    reservation = get_object_or_404(
        Reservation, id=id, user_id=request.user.id)
    context = {
        'setting': setting,
        'category': category,
        'menu': menu,
        'page': 'Reservation Detail',
        'reservation': reservation
    }
    return render(request, 'user_reservation_detail.html', context)


@login_required(login_url='/login')
def comments(request):
    setting = Setting.objects.first()
    category = Category.objects.filter(status=True)
    menu = Menu.objects.filter(status=True)
    comments = Comment.objects.filter(user_id=request.user.id)
    context = {
        'setting': setting,
        'category': category,
        'menu': menu,
        'comments': comments,
        'page': 'My Comments'
    }
    return render(request, 'user_comments.html', context)


@login_required(login_url='/login')
def delete_comment(request, id):
    Comment.objects.get(user_id=request.user.id, id=id).delete()
    messages.success(request, 'Message deleted!')
    return HttpResponseRedirect('/user/comments')


@login_required(login_url='/login')
def contents(request):
    setting = Setting.objects.first()
    category = Category.objects.filter(status=True)
    menu = Menu.objects.filter(status=True)
    contents = Content.objects.filter(user_id=request.user.id)
    context = {
        'setting': setting,
        'category': category,
        'menu': menu,
        'contents': contents,
        'page': 'My Contents'
    }
    return render(request, 'user_contents.html', context)


@login_required(login_url='/login')
def addcontent(request):
    if request.method == "POST":
        form = ContentForm(request.POST, request.FILES)
        if form.is_valid():
            data = Content()
            data.user_id = request.user.id
            data.title = form.cleaned_data['title']
            data.keywords = form.cleaned_data['keywords']
            data.description = form.cleaned_data['description']
            data.image = form.cleaned_data['image']
            data.kind = form.cleaned_data['kind']
            data.slug = form.cleaned_data['slug']
            data.detail = form.cleaned_data['detail']
            data.status = "False"
            data.save()
            messages.success(request, 'Content added!')
            return HttpResponseRedirect('/user/contents')
        else:
            messages.warning(request, 'Content Form Error:' + str(form.errors))
            return HttpResponseRedirect('/user/addcontent')
    else:
        setting = Setting.objects.first()
        category = Category.objects.filter(status=True)
        menu = Menu.objects.filter(status=True)
        form = ContentForm()
        context = {
            'setting': setting,
            'category': category,
            'menu': menu,
            'page': 'Add Content',
            'form': form
        }
        return render(request, 'user_addcontent.html', context)


@login_required(login_url='/login')
def contentedit(request, id):
    content = get_object_or_404(Content, id=id, user_id=request.user.id)
    if request.method == 'POST':
        form = ContentForm(request.POST, request.FILES, instance=content)
        if form.is_valid():
            form.save()
            messages.success(request, 'Content updated successfuly!')
            return HttpResponseRedirect('/user/contents')
        else:
            messages.warning(request, 'Content Form Error: '+str(form.errors))
            return HttpResponseRedirect('/user/contentedit/id')
    else:
        setting = Setting.objects.first()
        category = Category.objects.filter(status=True)
        menu = Menu.objects.filter(status=True)
        contents = Content.objects.filter(user_id=request.user.id)
        form = ContentForm(instance=content)
        context = {
            'setting': setting,
            'category': category,
            'menu': menu,
            'contents': contents,
            'form': form,
            'page': 'Edit Content'
        }
        return render(request, 'user_addcontent.html', context)


@login_required(login_url='/login')
def contentdelete(request, id):
    content = get_object_or_404(Content, id=id, user_id=request.user.id)
    content.delete()
    messages.success(request, 'Content deleted!')
    return HttpResponseRedirect('/user/contents')


@login_required(login_url='/login')
def contentaddimage(request, id):
    if request.method == 'POST':
        lasturl = request.META.get('HTTP_REFERER')
        form = CImagesForm(request.POST, request.FILES)
        if form.is_valid():
            data = CImages()
            data.title = form.cleaned_data['title']
            data.image = form.cleaned_data['image']
            data.content_id = id
            data.save()
            messages.success(request, 'Image has been successfully uploaded!')
            return HttpResponseRedirect(lasturl)
        else:
            messages.warning(request, 'Form Error:' + str(form.errors))
            return HttpResponseRedirect(lasturl)
    else:
        content = get_object_or_404(Content, id=id)
        try:
            images = CImages.objects.filter(content_id=id)
        except:
            images = []
        form = CImagesForm()
        context = {
            'content': content,
            'images': images,
            'form': form
        }
        return render(request, 'user_content_gallery.html', context)
