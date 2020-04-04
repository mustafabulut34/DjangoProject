from django.shortcuts import render
from .models import Setting


def index(request):
    setting = Setting.objects.first()
    return render(request, 'index.html', {'setting': setting})


def aboutus(request):
    setting = Setting.objects.first()
    return render(request, 'aboutus.html', {'setting': setting})


def references(request):
    setting = Setting.objects.first()
    return render(request, 'references.html', {'setting': setting})


def contact(request):
    setting = Setting.objects.first()
    return render(request, 'contact.html', {'setting': setting})
