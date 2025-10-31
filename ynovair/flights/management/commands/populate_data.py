from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from flights.models import Airport, Flight
import random


class Command(BaseCommand):
    help = 'Populate database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating airports...')

        # Créer des aéroports
        airports_data = [
            {'code': 'CDG', 'name': 'Aéroport Charles de Gaulle', 'city': 'Paris', 'country': 'France'},
            {'code': 'LYS', 'name': 'Aéroport Lyon-Saint Exupéry', 'city': 'Lyon', 'country': 'France'},
            {'code': 'MRS', 'name': 'Aéroport Marseille Provence', 'city': 'Marseille', 'country': 'France'},
            {'code': 'TLS', 'name': 'Aéroport Toulouse-Blagnac', 'city': 'Toulouse', 'country': 'France'},
            {'code': 'NCE', 'name': 'Aéroport Nice Côte d\'Azur', 'city': 'Nice', 'country': 'France'},
            {'code': 'NTE', 'name': 'Aéroport Nantes Atlantique', 'city': 'Nantes', 'country': 'France'},
            {'code': 'BOD', 'name': 'Aéroport de Bordeaux-Mérignac', 'city': 'Bordeaux', 'country': 'France'},
            {'code': 'BCN', 'name': 'Aéroport de Barcelone', 'city': 'Barcelone', 'country': 'Espagne'},
            {'code': 'MAD', 'name': 'Aéroport Madrid-Barajas', 'city': 'Madrid', 'country': 'Espagne'},
            {'code': 'LHR', 'name': 'Aéroport de Londres Heathrow', 'city': 'Londres', 'country': 'Royaume-Uni'},
        ]

        airports = {}
        for airport_data in airports_data:
            airport, created = Airport.objects.get_or_create(**airport_data)
            airports[airport.code] = airport
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created airport: {airport}'))

        self.stdout.write('Creating flights...')

        # Créer des vols
        routes = [
            ('CDG', 'LYS'), ('LYS', 'CDG'),
            ('CDG', 'MRS'), ('MRS', 'CDG'),
            ('CDG', 'TLS'), ('TLS', 'CDG'),
            ('CDG', 'NCE'), ('NCE', 'CDG'),
            ('LYS', 'MRS'), ('MRS', 'LYS'),
            ('LYS', 'TLS'), ('TLS', 'LYS'),
            ('CDG', 'BCN'), ('BCN', 'CDG'),
            ('CDG', 'MAD'), ('MAD', 'CDG'),
            ('CDG', 'LHR'), ('LHR', 'CDG'),
            ('LYS', 'BCN'), ('BCN', 'LYS'),
        ]

        flight_number = 100
        for origin_code, dest_code in routes:
            origin = airports[origin_code]
            destination = airports[dest_code]

            # Créer plusieurs vols pour chaque route
            for day in range(7):
                for hour in [8, 12, 16, 20]:
                    departure_time = timezone.now() + timedelta(days=day, hours=hour)
                    duration = timedelta(hours=random.randint(1, 3), minutes=random.randint(0, 59))
                    arrival_time = departure_time + duration

                    total_seats = random.choice([150, 180, 200, 250])
                    available_seats = random.randint(int(total_seats * 0.3), total_seats)
                    price = random.randint(50, 300)

                    flight, created = Flight.objects.get_or_create(
                        flight_number=f'YN{flight_number}',
                        defaults={
                            'origin': origin,
                            'destination': destination,
                            'departure_time': departure_time,
                            'arrival_time': arrival_time,
                            'duration': duration,
                            'available_seats': available_seats,
                            'total_seats': total_seats,
                            'price': price,
                            'status': 'SCHEDULED'
                        }
                    )

                    if created:
                        self.stdout.write(f'Created flight: {flight}')

                    flight_number += 1

        self.stdout.write(self.style.SUCCESS('Successfully populated database!'))
