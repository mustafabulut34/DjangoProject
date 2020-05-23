from django.db import models
from hotel.models import Room
from user.models import User
from django.forms import ModelForm
# Create your models here.


class Reservation(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Canceled', 'Canceled'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    phone = models.CharField(blank=True, max_length=30)
    admin_note = models.CharField(blank=True, max_length=255)
    total = models.IntegerField()
    checkin = models.DateField(blank=False)
    checkout = models.DateField(blank=False)
    days = models.IntegerField(blank=True, default=1)

    ip = models.CharField(max_length=20)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.room.title


class ReservationForm(ModelForm):
    class Meta:
        model = Reservation
        fields = ['name', 'surname', 'phone', 'checkin', 'days']
