from django.shortcuts import render
from .models import Setting


def index(request):
    setting = Setting.objects.first()
    return render(request, 'index.html', {'setting': setting})
