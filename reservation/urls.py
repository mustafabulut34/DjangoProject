from django.urls import path
from reservation import views

urlpatterns = [
    path('<int:id>/<slug:slug>', views.index, name="index"),
    path('new_reservation/<int:id>', views.new_reservation, name="new_reservation"),
    path('book/<int:id>', views.book, name='book'),
    path('reservationdelete/<int:id>',
         views.reservation_delete, name="reservation_delete"),
]
