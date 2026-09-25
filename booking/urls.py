from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('rooms/<int:room_id>/book/', views.book_room, name='book_room'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('my-bookings/<int:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
]
