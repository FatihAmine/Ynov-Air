from django.contrib import admin
from .models import Airport, Flight, Passenger, Booking


@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'city', 'country')
    search_fields = ('code', 'name', 'city')


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('flight_number', 'origin', 'destination', 'departure_time', 'price', 'available_seats', 'status')
    list_filter = ('status', 'origin', 'destination')
    search_fields = ('flight_number',)


@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone')
    search_fields = ('first_name', 'last_name', 'email')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_reference', 'flight', 'passenger', 'booking_date', 'total_price', 'status')
    list_filter = ('status', 'booking_date')
    search_fields = ('booking_reference', 'passenger__first_name', 'passenger__last_name')
