from django.shortcuts import render
from .models import Setting, ContactForm, ContactFormMessage
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from hotel.models import Hotel, Category, Room, ImageRoom, CommentForm, Comment
from .forms import SearchForm


def index(request):
    setting = Setting.objects.first()
    page = 'index'
    category = Category.objects.all()
    slides = Hotel.objects.all()[:5]
    rooms = Room.objects.all().order_by('?')[:6]
    context = {
        'setting': setting,
        'slides': slides,
        'page': page,
        'category': category,
        'rooms': rooms}
    return render(request, 'index.html', context)


def category(request, slug, id):
    setting = Setting.objects.first()
    getCat = Category.objects.get(id=id)
    page = str(getCat.title)
    rooms = Room.objects.filter(hotel_id__category=getCat)
    category = Category.objects.all()
    context = {'setting': setting, 'rooms': rooms,
               'page': page, 'category': category}
    return render(request, 'rooms.html', context)


def hotel(request, slug, id):
    setting = Setting.objects.first()
    category = Category.objects.all()
    rooms = Room.objects.get(hotel_id=id)
    page = rooms.hotel_id
    context = {
        'setting': setting,
        'page': page,
        'category': category,
        'rooms': rooms
    }
    return render(request, 'index.html', context)


def room(request, hotelslug, roomslug, id):
    setting = Setting.objects.first()
    room = Room.objects.get(id=id)
    images = ImageRoom.objects.filter(room_id=id)
    page = 'room'
    category = Category.objects.all()
    comments = Comment.objects.filter(
        room_id=id, status=True).order_by('-created_at')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            data = Comment()
            data.rate = form.cleaned_data['rate']
            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, "Thank you!")
            return HttpResponseRedirect('')
    form = CommentForm()
    context = {
        'setting': setting,
        'page': page,
        'category': category,
        'room': room,
        'images': images,
        'form': form,
        'comments': comments
    }
    return render(request, 'room_detail.html', context)


def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            category = Category.objects.all()
            query = form.cleaned_data['query']
            rooms = Room.objects.filter(title__icontains=query)
            context = {
                'category': category,
                'rooms': rooms,
                'page': 'Search Rooms',
                'lastForm': query
            }
            return render(request, 'rooms_search.html', context)
    return HttpResponseRedirect("/")


def aboutus(request):
    setting = Setting.objects.first()
    page = 'About'
    category = Category.objects.all()

    context = {'setting': setting, 'page': page, 'category': category}
    return render(request, 'aboutus.html', context)


def references(request):
    setting = Setting.objects.first()
    page = 'References'
    category = Category.objects.all()

    context = {'setting': setting, 'page': page, 'category': category}
    return render(request, 'references.html', context)


def contact(request):
    setting = Setting.objects.first()
    page = 'Contact'
    category = Category.objects.all()

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
    context = {'setting': setting, 'form': form,
               'page': page, 'category': category}
    return render(request, 'contact.html', context)
