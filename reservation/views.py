from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from home.models import Setting
from hotel.models import Category, Room
from .models import Reservation, ReservationForm
from user.models import UserProfile
from datetime import date, timedelta
from .forms import ReservationDayForm
from django.contrib import messages
# Create your views here.


def index(request, id):
    return HttpResponse('Room: ' + id)


@login_required(login_url='/login')
def new_reservation(request, id):
    days = 1
    checkin = date.today()

    if request.method == 'POST':
        form = ReservationDayForm(request.POST)
        if form.is_valid():
            days = form.cleaned_data['days']
            checkin = form.cleaned_data['checkin']

    setting = Setting.objects.first()
    page = 'New Reservation'
    category = Category.objects.filter(status=True)
    profile = get_object_or_404(UserProfile, user=request.user)
    room = get_object_or_404(Room, id=id, status=True)
    total = room.price * days

    form = ReservationForm()
    form.initial["days"] = days
    form.initial['checkin'] = checkin
    form.initial['name'] = profile.user.first_name
    form.initial['surname'] = profile.user.last_name
    form.initial['phone'] = profile.phone

    context = {
        'setting': setting,
        'category': category,
        'page': page,
        'form': form,
        'room': room,
        'profile': profile,
        'total': total
    }
    return render(request, 'new_reservation.html', context)


@login_required(login_url='/login')
def book(request, id):
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = Reservation()
            reservation.user = request.user
            reservation.room = get_object_or_404(Room, id=id)
            reservation.name = form.cleaned_data['name']
            reservation.surname = form.cleaned_data['surname']
            reservation.phone = form.cleaned_data['phone']
            reservation.checkin = form.cleaned_data['checkin']
            reservation.days = form.cleaned_data['days']
            reservation.checkout = reservation.checkin + \
                timedelta(days=reservation.days)
            reservation.total = reservation.room.price * reservation.days
            reservation.ip = request.META.get('REMOTE_ADDR')
            reservation.save()
            messages.success(request, "Reservation created!")
    return HttpResponseRedirect('/user/reservations')


@login_required(login_url='/login')
def reservation_delete(request, id):
    reservation = get_object_or_404(
        Reservation, id=id, user_id=request.user.id)

    if(reservation.status == "New"):
        reservation.delete()
        messages.success(request, 'Reservation deleted!')
    else:
        messages.warning(
            request, "Cannot cancel this reservation! Only can delete reservation which one status is new!")

    return HttpResponseRedirect("/user/reservations")
