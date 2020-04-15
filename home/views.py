from django.shortcuts import render
from .models import Setting, ContactForm, ContactFormMessage
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from hotel.models import Hotel


def index(request):
    setting = Setting.objects.first()
    page = 'index'

    slides = Hotel.objects.all()[:5]
    context = {'setting': setting, 'slides': slides, 'page': page}
    return render(request, 'index.html', context)


def hotel(request, id, slug):
    setting = Setting.objects.first()
    page = 'index'

    slides = Hotel.objects.all()[:5]
    context = {'setting': setting, 'slides': slides, 'page': page}
    return render(request, 'index.html', context)


def aboutus(request):
    setting = Setting.objects.first()
    page = 'About'

    context = {'setting': setting, 'page': page}
    return render(request, 'aboutus.html', context)


def references(request):
    setting = Setting.objects.first()
    page = 'References'

    context = {'setting': setting, 'page': page}
    return render(request, 'references.html', context)


def contact(request):
    setting = Setting.objects.first()
    page = 'Contact'

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
    context = {'setting': setting, 'form': form, 'page': page}
    return render(request, 'contact.html', context)
