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
    path('deletecomment/<int:id>', views.delete_comment, name="delete_comment"),
    path('addcontent/', views.addcontent, name="addcontent"),
    path('contents/', views.contents, name="contents"),
    path('contentedit/<int:id>', views.contentedit, name="contentedit"),
    path('contentdelete/<int:id>', views.contentdelete, name="contentdelete"),
    path('contentaddimage/<int:id>', views.contentaddimage, name="contentaddimage"),
]
