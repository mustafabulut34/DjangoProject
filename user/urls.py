from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('update/', views.update, name="update"),
    path('password/', views.change_password, name="change_password"),
    path('reservations/', views.reservations, name="reservations"),
    path('reservationdetail/<int:id>',
         views.reservation_detail, name="reservation_detail"),
    path('comments/', views.comments, name="comments"),
]
