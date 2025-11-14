from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .models import Flight, Airport, Passenger, Booking
import random
import string
from django.contrib.auth.decorators import login_required


def home(request):
    """Page d'accueil avec recherche de vols"""
    airports = Airport.objects.all()
    upcoming_flights = Flight.objects.filter(
        departure_time__gte=timezone.now(),
        status='SCHEDULED'
    ).order_by('departure_time')[:6]

    context = {
        'airports': airports,
        'upcoming_flights': upcoming_flights,
    }
    return render(request, 'flights/home.html', context)


def search_flights(request):
    """Recherche de vols"""
    flights = []

    if request.method == 'GET':
        origin_id = request.GET.get('origin')
        destination_id = request.GET.get('destination')
        date = request.GET.get('date')

        if origin_id and destination_id:
            flights = Flight.objects.filter(
                origin_id=origin_id,
                destination_id=destination_id,
                status='SCHEDULED'
            )

            if date:
                flights = flights.filter(departure_time__date=date)

            flights = flights.order_by('departure_time')

    airports = Airport.objects.all()
    context = {
        'flights': flights,
        'airports': airports,
    }
    return render(request, 'flights/search.html', context)


def flight_detail(request, flight_id):
    """Détails d'un vol"""
    flight = get_object_or_404(Flight, id=flight_id)
    context = {'flight': flight}
    return render(request, 'flights/flight_detail.html', context)

@login_required
def booking_create(request, flight_id):
    """Créer une réservation"""
    flight = get_object_or_404(Flight, id=flight_id)

    if request.method == 'POST':
        # Créer le passager
        passenger = Passenger.objects.create(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            passport_number=request.POST.get('passport_number'),
            date_of_birth=request.POST.get('date_of_birth')
        )

        # Générer une référence unique
        booking_reference = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

        # Créer la réservation
        number_of_passengers = int(request.POST.get('number_of_passengers', 1))

        if flight.available_seats >= number_of_passengers:
            booking = Booking.objects.create(
                booking_reference=booking_reference,
                flight=flight,
                passenger=passenger,
                user=request.user,
                number_of_passengers=number_of_passengers,
                total_price=flight.price * number_of_passengers,
                status='CONFIRMED'
            )

            messages.success(request, f'Réservation confirmée ! Référence: {booking_reference}')
            return redirect('booking_detail', booking_id=booking.id)
        else:
            messages.error(request, 'Pas assez de sièges disponibles.')

    context = {'flight': flight}
    return render(request, 'flights/booking_create.html', context)


def booking_detail(request, booking_id):
    """Détails d'une réservation"""
    booking = get_object_or_404(Booking, id=booking_id)
    context = {'booking': booking}
    return render(request, 'flights/booking_detail.html', context)


def my_bookings(request):
    """Liste des réservations"""
    bookings = Booking.objects.all().order_by('-booking_date')
    context = {'bookings': bookings}
    return render(request, 'flights/my_bookings.html', context)
