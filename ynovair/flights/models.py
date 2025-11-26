from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


class Airport(models.Model):
    """Modèle représentant un aéroport"""
    code = models.CharField(max_length=3, unique=True, verbose_name="Code IATA")
    name = models.CharField(max_length=200, verbose_name="Nom de l'aéroport")
    city = models.CharField(max_length=100, verbose_name="Ville")
    country = models.CharField(max_length=100, verbose_name="Pays")

    class Meta:
        verbose_name = "Aéroport"
        verbose_name_plural = "Aéroports"
        ordering = ['city']

    def __str__(self):
        return f"{self.code} - {self.city}"


class Flight(models.Model):
    """Modèle représentant un vol"""
    STATUS_CHOICES = [
        ('SCHEDULED', 'Programmé'),
        ('BOARDING', 'Embarquement'),
        ('DEPARTED', 'Décollé'),
        ('LANDED', 'Atterri'),
        ('CANCELLED', 'Annulé'),
    ]

    flight_number = models.CharField(max_length=10, unique=True, verbose_name="Numéro de vol")
    airline = models.CharField(max_length=100, verbose_name="Airline") 
    origin = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name='departures',
        verbose_name="Aéroport de départ"
    )
    destination = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name='arrivals',
        verbose_name="Aéroport d'arrivée"
    )
    departure_time = models.DateTimeField(verbose_name="Heure de départ")
    arrival_time = models.DateTimeField(verbose_name="Heure d'arrivée")
    duration = models.DurationField(verbose_name="Durée du vol")
    available_seats = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(300)],
        verbose_name="Sièges disponibles"
    )
    total_seats = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(300)],
        verbose_name="Sièges totaux"
    )
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Prix (€)"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='SCHEDULED',
        verbose_name="Statut"
    )

    class Meta:
        verbose_name = "Vol"
        verbose_name_plural = "Vols"
        ordering = ['departure_time']

    def __str__(self):
        return f"{self.flight_number} - {self.origin.code} > {self.destination.code}"

    def is_available(self):
        """Vérifie si le vol a des sièges disponibles"""
        return self.available_seats > 0 and self.status == 'SCHEDULED'

    def get_occupancy_rate(self):
        """Calcule le taux d'occupation du vol"""
        if self.total_seats > 0:
            return ((self.total_seats - self.available_seats) / self.total_seats) * 100
        return 0


class Passenger(models.Model):
    """Modèle représentant un passager"""
    first_name = models.CharField(max_length=100, verbose_name="Prénom")
    last_name = models.CharField(max_length=100, verbose_name="Nom")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Téléphone")
    passport_number = models.CharField(max_length=20, verbose_name="Numéro de passeport")
    date_of_birth = models.DateField(verbose_name="Date de naissance")

    class Meta:
        verbose_name = "Passager"
        verbose_name_plural = "Passagers"
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_full_name(self):
        """Retourne le nom complet du passager"""
        return f"{self.first_name} {self.last_name}"


class Booking(models.Model):
    """Modèle représentant une réservation"""
    STATUS_CHOICES = [
        ('PENDING', 'En attente'),
        ('CONFIRMED', 'Confirmée'),
        ('CANCELLED', 'Annulée'),
        ('COMPLETED', 'Terminée'),
    ]

    booking_reference = models.CharField(
        max_length=8,
        unique=True,
        verbose_name="Référence de réservation"
    )
    flight = models.ForeignKey(
        Flight,
        on_delete=models.CASCADE,
        related_name='bookings',
        verbose_name="Vol"
    )
    passenger = models.ForeignKey(
        Passenger,
        on_delete=models.CASCADE,
        related_name='bookings',
        verbose_name="Passager"
    )
    booking_date = models.DateTimeField(auto_now_add=True, verbose_name="Date de réservation")
    number_of_passengers = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name="Nombre de passagers"
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Prix total (€)"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING',
        verbose_name="Statut"
    )
    seat_number = models.CharField(
        max_length=5,
        blank=True,
        null=True,
        verbose_name="Numéro de siège"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)


    class Meta:
        verbose_name = "Réservation"
        verbose_name_plural = "Réservations"
        ordering = ['-booking_date']

    def __str__(self):
        return f"{self.booking_reference} - {self.passenger.get_full_name()}"

    def save(self, *args, **kwargs):
        """Override save pour gérer la disponibilité des sièges"""
        if not self.pk:  # Nouvelle réservation
            if self.flight.available_seats >= self.number_of_passengers:
                self.flight.available_seats -= self.number_of_passengers
                self.flight.save()
        super().save(*args, **kwargs)

    def cancel(self):
        """Annule la réservation et libère les sièges"""
        if self.status != 'CANCELLED':
            self.status = 'CANCELLED'
            self.flight.available_seats += self.number_of_passengers
            self.flight.save()
            self.save()


class Review(models.Model):
    """Modèle représentant une évaluation d'un vol par un utilisateur"""

    RATING_CHOICES = [
        (1, "1 - Très mauvais"),
        (2, "2 - Mauvais"),
        (3, "3 - Moyen"),
        (4, "4 - Bon"),
        (5, "5 - Excellent"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Utilisateur"
    )
    flight = models.ForeignKey(
        Flight,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Vol"
    )
    rating = models.IntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Note"
    )
    comment = models.TextField(
        max_length=500,
        blank=True,
        verbose_name="Commentaire"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")

class Meta:
    verbose_name = "Avis"
    verbose_name_plural = "Avis"
    ordering = ['-created_at']
