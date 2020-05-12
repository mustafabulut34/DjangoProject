from django.shortcuts import render
from django.http import HttpResponse
from hotel.models import Category
from home.models import Setting
from .models import UserProfile
from django.contrib.auth.decorators import login_required


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
