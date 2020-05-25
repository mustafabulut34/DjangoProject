from django.shortcuts import render, get_object_or_404
from .models import Setting, ContactForm, ContactFormMessage, Faq
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from hotel.models import Hotel, Category, Room, ImageRoom, CommentForm, Comment
from content.models import Menu, Content, CImages
from .forms import SearchForm, SignUpForm
from reservation.forms import ReservationDayForm
from user.models import UserProfile
import json


def index(request):
    setting = Setting.objects.first()
    page = 'index'
    category = Category.objects.filter(status=True)
    menu = Menu.objects.filter(status=True)
    campaigns = Content.objects.filter(
        kind='Campaign', status=True).order_by('-id')[:3]
    slides = Hotel.objects.filter(status=True)[:5]
    rooms = Room.objects.filter(
        status=True, hotel_id__status=True).order_by('?')[:6]
    context = {
        'campaigns': campaigns,
        'setting': setting,
        'slides': slides,
        'page': page,
        'menu': menu,
        'category': category,
        'rooms': rooms}
    return render(request, 'index.html', context)


def category(request, slug, id):
    setting = Setting.objects.first()
    getCat = get_object_or_404(Category, id=id, status=True)
    page = str(getCat.title)
    rooms = Room.objects.filter(
        hotel_id__category=getCat, status=True, hotel_id__status=True)
    category = Category.objects.filter(status=True)
    menu = Menu.objects.filter(status=True)
    context = {
        'setting': setting,
        'menu': menu,
        'rooms': rooms,
        'page': page,
        'category': category}
    return render(request, 'rooms.html', context)


def all_category(request):
    setting = Setting.objects.first()
    page = 'All Rooms'
    rooms = Room.objects.filter(status=True, hotel_id__status=True)
    category = Category.objects.filter(status=True)
    menu = Menu.objects.filter(status=True)
    context = {
        'setting': setting,
        'menu': menu,
        'rooms': rooms,
        'page': page,
        'category': category}
    return render(request, 'rooms.html', context)


def hotel(request, slug, id):
    setting = Setting.objects.first()
    category = Category.objects.filter(status=True)
    rooms = Room.objects.filter(
        hotel_id=id, status=True, hotel_id__status=True)
    page = rooms.first().hotel_id.title
    menu = Menu.objects.filter(status=True)
    context = {
        'setting': setting,
        'menu': menu,
        'page': page,
        'category': category,
        'rooms': rooms,
        'pageControl': 'HOTEL',
    }
    return render(request, 'rooms.html', context)


def room(request, hotelslug, roomslug, id):
    setting = Setting.objects.first()
    menu = Menu.objects.filter(status=True)
    room = get_object_or_404(Room, id=id, status=True, hotel_id__status=True)
    images = ImageRoom.objects.filter(room_id=id)
    page = 'room'
    category = Category.objects.filter(status=True)
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
    reservationForm = ReservationDayForm()
    context = {
        'setting': setting,
        'menu': menu,
        'page': page,
        'category': category,
        'room': room,
        'images': images,
        'form': form,
        'comments': comments,
        'reservationForm': reservationForm
    }
    return render(request, 'room_detail.html', context)


def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            category = Category.objects.filter(status=True)
            menu = Menu.objects.filter(status=True)
            query = form.cleaned_data['query']
            catid = form.cleaned_data['catid']
            if catid != 0:
                rooms = Room.objects.filter(
                    title__icontains=query, hotel_id__category=catid, hotel_id__status=True, status=True)
            else:
                rooms = Room.objects.filter(
                    title__icontains=query, status=True, hotel_id__status=True)
            context = {
                'category': category,
                'menu': menu,
                'rooms': rooms,
                'page': 'Search Rooms',
                'lastForm': form
            }
            return render(request, 'rooms_search.html', context)
    return HttpResponseRedirect("/")


def search_box(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        rooms = Room.objects.filter(
            title__icontains=q, status=True, hotel_id__status=True)
        results = []
        for room in rooms:
            room_json = {}
            room_json = room.title
            results.append(room_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            # Redirect to a success page.
            messages.success(request, "Login succesfully!")
            url = '/'
        else:
            # Return an 'invalid login' error message.
            messages.warning(request, "Wrong username or password!")
            url = '/login'
        return HttpResponseRedirect(url)
    setting = Setting.objects.first()
    category = Category.objects.filter(status=True)
    menu = Menu.objects.filter(status=True)
    context = {
        'setting': setting,
        'menu': menu,
        'page': 'Login',
        'category': category,
        'menu': menu,
    }
    return render(request, 'login.html', context)


def logout(request):
    auth_logout(request)
    messages.success(request, "Logout succesfully!")
    return HttpResponseRedirect("/")


def sign_up(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        print("FORM OKEY!")
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            auth_login(request, user)
            data = UserProfile()
            data.user_id = request.user.id
            data.image = "images/users/user.png"
            data.save()
            messages.success(request, "Sign up successfully!")
            return HttpResponseRedirect("/")
        else:
            messages.warning(request, "Check Form! " + str(form.errors))
            return HttpResponseRedirect("/signup")
    print("POST DEĞİL")
    form = SignUpForm()
    setting = Setting.objects.first()
    category = Category.objects.filter(status=True)
    menu = Menu.objects.filter(status=True)
    context = {
        'setting': setting,
        'menu': menu,
        'page': 'Sign Up',
        'category': category,
        'form': form
    }
    return render(request, 'sign_up.html', context)


def aboutus(request):
    setting = Setting.objects.first()
    page = 'About'
    category = Category.objects.filter(status=True)
    menu = Menu.objects.filter(status=True)
    context = {
        'setting': setting,
        'page': page,
        'menu': menu,
        'category': category
    }
    return render(request, 'aboutus.html', context)


def references(request):
    setting = Setting.objects.first()
    page = 'References'
    category = Category.objects.filter(status=True)
    menu = Menu.objects.filter(status=True)
    context = {
        'setting': setting,
        'page': page,
        'category': category,
        'menu': menu
    }
    return render(request, 'references.html', context)


def contact(request):
    setting = Setting.objects.first()
    page = 'Contact'
    category = Category.objects.filter(status=True)
    menu = Menu.objects.filter(status=True)
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
    context = {
        'setting': setting,
        'form': form,
        'page': page,
        'category': category,
        'menu': menu,
    }
    return render(request, 'contact.html', context)


def menu(request, id):
    content = get_object_or_404(Content, menu_id=id, status=True)
    link = '/content/' + str(content.id)+'/menu'
    return HttpResponseRedirect(link)


def contentdetail(request, id, slug):
    setting = Setting.objects.first()
    category = Category.objects.filter(status=True)
    menu = Menu.objects.filter(status=True)
    content = get_object_or_404(Content, id=id, status=True)
    images = CImages.objects.filter(content_id=id)
    page = str(content.title)

    context = {
        'setting': setting,
        'content': content,
        'category': category,
        'menu': menu,
        'images': images,
        'page': page
    }
    return render(request, 'content_detail.html', context)


def faq(request):
    setting = Setting.objects.first()
    category = Category.objects.filter(status=True)
    menu = Menu.objects.filter(status=True)
    faqs = Faq.objects.filter(status=True).order_by('ordernumber')
    context = {
        'setting': setting,
        'category': category,
        'menu': menu,
        'faqs': faqs,
        'page': 'FAQ'
    }
    return render(request, 'faq.html', context)
