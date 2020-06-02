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
from django.db.models import Q


def index(request, id):
    return HttpResponse('Room: ' + id)


def get_earliest_date(id):
    Reservation.objects.filter(
        room__id=id, checkout__lte=date.today()).update(status='Finished')

    reservations = Reservation.objects.filter(
        room__id=id, checkout__gt=date.today()).order_by('checkout')

    for reservation in reservations:
        if len(reservations.filter(checkout=reservation.checkout)) > len(reservations.filter(checkin=reservation.checkout)):
            return reservation
    return reservations.last()


def latest_checkin_reservation(id, reservation_count, chechkindate):
    reservations = Reservation.objects.filter(
        room__id=id, checkin__gt=chechkindate).order_by('checkin')
    if reservations:
        return reservations.first()
    return -1


@login_required(login_url='/login')
def new_reservation(request, id):
    days = 1
    checkin = date.today()

    if request.method == 'POST':
        form = ReservationDayForm(request.POST)
        if form.is_valid():
            days = form.cleaned_data['days']
            checkin = form.cleaned_data['checkin']
        else:
            messages.warning(request, str(form.errors))
            return HttpResponseRedirect("/reservation/new_reservation/"+id)
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
            reservation.checkin = form.cleaned_data['checkin']
            reservation.days = form.cleaned_data['days']
            reservation.checkout = reservation.checkin + \
                timedelta(days=reservation.days)

            earliest_checkout_reservation = get_earliest_date(
                id)
            activate_stay_count = len(Reservation.objects.filter(
                room_id=id, status__in=['New', 'Accepted'], checkin__lte=date.today()))
            if activate_stay_count >= reservation.room.count:
                if reservation.checkin < earliest_checkout_reservation.checkout:
                    messages.warning(request, "Sorry. We cannot reservate this room. No empty room on this day! You can book earliest date -> " + str(
                        earliest_checkout_reservation.checkout.strftime("%d %B, %Y")))
                    return HttpResponseRedirect("/room/"+str(id)+"/"+reservation.room.hotel_id.slug+"-"+reservation.room.slug)
                else:
                    latest_checkin = latest_checkin_reservation(
                        id, activate_stay_count, reservation.checkin)
                    if latest_checkin != -1:
                        if reservation.checkout > latest_checkin.checkin:
                            messages.warning(request, "Sorry. We cannot reservate this room. You can book this room on date from " + str(
                                reservation.checkin.strftime("%d %B, %Y")) + " to "+str(latest_checkin.checkin.strftime("%d %B, %Y")))
                            return HttpResponseRedirect("/room/"+str(id)+"/"+reservation.room.hotel_id.slug+"-"+reservation.room.slug)
            reservation.name = form.cleaned_data['name']
            reservation.surname = form.cleaned_data['surname']
            reservation.phone = form.cleaned_data['phone']

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
