from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Place(models.Model):
    name = models.CharField(max_length=200)  # Name of the place (e.g., street or neighborhood)
    country = models.CharField(max_length=100)  # Country name
    city = models.CharField(max_length=100, blank=True, null=True)  # City (optional)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)  # Latitude for GPS
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)  # Longitude for GPS
    description = models.TextField(blank=True, null=True)  # Additional description for the location

    class Meta:
        verbose_name_plural = "Places"

    def __str__(self):
        return f"{self.name}, {self.country}"

class Hotel(models.Model):
    name = models.CharField(max_length=200)  # Name of the hotel
    place = models.ForeignKey('Place', on_delete=models.CASCADE, related_name='hotels')  # Link to the Place model
    rating = models.DecimalField(blank=True, null=True, max_digits=4, decimal_places=1)  # Rating (e.g., 4 stars)
    number_of_rooms = models.PositiveIntegerField()  # Number of rooms in the hotel
    available_rooms = models.PositiveIntegerField()  # Number of available rooms
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)  # Price per night
    amenities = models.TextField(blank=True, null=True)  # Amenities list (optional, comma-separated or as a string)
    description = models.TextField(blank=True, null=True)  # Additional description for the hotel

    class Meta:
        verbose_name_plural = "Hotels"

    def __str__(self):
        return f"{self.name} - {self.place.name}"


class Review(models.Model):
    hotel = models.ForeignKey('Hotel', on_delete=models.CASCADE, related_name='reviews')  # Link to the Hotel model
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')  # The user who wrote the review
    rating = models.PositiveIntegerField()  # Rating given by the user (1-5 stars)
    content = models.TextField()  # The body of the review
    created_at = models.DateTimeField(auto_now_add=True)  # Date and time when the review was created
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)  # Date and time when the review was last updated

    class Meta:
        verbose_name_plural = "Reviews"
        ordering = ['-created_at']  # Order by newest reviews first

    def __str__(self):
        return f"Review by {self.user.username} for {self.hotel.name} - {self.rating} stars"

