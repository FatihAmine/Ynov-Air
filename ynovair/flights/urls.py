from django.urls import path
from . import views

from .auth_views import (
    register_view,
    login_view,
    logout_view,
    profile_view,
    profile_update_view
)

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search_flights, name='search_flights'),
    path('flight/<int:flight_id>/', views.flight_detail, name='flight_detail'),
    path('flight/<int:flight_id>/book/', views.booking_create, name='booking_create'),
    path('booking/<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),

    # Authentification
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('profile/update/', profile_update_view, name='profile_update'),
]
