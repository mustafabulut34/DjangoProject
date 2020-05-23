from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.utils.html import mark_safe
from django.forms import TextInput, FileInput


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(blank=True, max_length=20)
    address = models.CharField(blank=True, max_length=150)
    city = models.CharField(blank=True, max_length=20)
    country = models.CharField(blank=True, max_length=20)
    image = models.ImageField(blank=True, upload_to='images/users/')

    def __str__(self):
        return self.user.username

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'

    def email(self):
        return self.user.email


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'city', 'country', 'image']
        widgets = {
            'phone':   TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
            'address':   TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            'city':   TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'country':   TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
            'image':   FileInput(attrs={'class': 'form-control', 'placeholder': 'Image'})
        }
