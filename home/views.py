from django.shortcuts import render
from .models import Setting, ContactForm, ContactFormMessage
from django.http import HttpResponseRedirect
from django.contrib import messages
from hotel.models import Hotel


def index(request):
    setting = Setting.objects.first()
    sliderData = Hotel.objects.all()[:5]
    return render(request, 'index.html', {'setting': setting, 'sliderData': sliderData})


def hotel(request, id, slug):
    setting = Setting.objects.first()
    sliderData = Hotel.objects.all()[:5]
    return render(request, 'index.html', {'setting': setting, 'sliderData': sliderData})


def aboutus(request):
    setting = Setting.objects.first()
    return render(request, 'aboutus.html', {'setting': setting})


def references(request):
    setting = Setting.objects.first()
    return render(request, 'references.html', {'setting': setting})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactFormMessage()
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, "Your message has been sent. Thank you!")
            return HttpResponseRedirect('/contact')

    form = ContactForm()
    setting = Setting.objects.first()
    context = {'setting': setting, 'form': form}
    return render(request, 'contact.html', context)
