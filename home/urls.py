from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('category/<int:id>/<slug:slug>', views.category, name="category"),
    path('hotel/<int:id>/<slug:slug>', views.hotel, name="hotel"),
    path('room/<int:id>/<slug:hotelslug>-<slug:roomslug>', views.room, name="room"),
    path('aboutus/', views.aboutus, name="aboutus"),
    path('references/', views.references, name="references"),
    path('contact/', views.contact, name="contact"),
]
