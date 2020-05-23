from django.urls import path
from home import views

urlpatterns = [
    path('', views.index, name="index"),
    path('category/<int:id>/<slug:slug>', views.category, name="category"),
    path('category/all-rooms', views.all_category, name="all-category"),
    path('hotel/<int:id>/<slug:slug>', views.hotel, name="hotel"),
    path('room/<int:id>/<slug:hotelslug>-<slug:roomslug>', views.room, name="room"),
    path('aboutus/', views.aboutus, name="aboutus"),
    path('references/', views.references, name="references"),
    path('contact/', views.contact, name="contact"),
    path('search/', views.search, name="search"),
    path('search_box/', views.search_box, name="search_box"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('signup/', views.sign_up, name="sign_up")

]
