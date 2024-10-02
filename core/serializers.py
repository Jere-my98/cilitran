from rest_framework import serializers
from .models import Place, Hotel, Review
from django.contrib.auth.models import User

# Place Serializer
class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ['id', 'name', 'country', 'region', 'city', 'address', 'postal_code', 'latitude', 'longitude', 'description']


# Hotel Serializer
class HotelSerializer(serializers.ModelSerializer):
    place = PlaceSerializer(read_only=True)  # Nested serializer to include place details
    place_id = serializers.PrimaryKeyRelatedField(queryset=Place.objects.all(), source='place', write_only=True)  # To allow setting place by ID

    class Meta:
        model = Hotel
        fields = ['id', 'name', 'place', 'place_id', 'address', 'rating', 'number_of_rooms', 'available_rooms', 'price_per_night', 'amenities', 'description']


# Review Serializer
class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # Show username in reviews
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user', write_only=True)  # Allow setting user by ID
    hotel = HotelSerializer(read_only=True)  # Nested hotel serializer to display hotel details
    hotel_id = serializers.PrimaryKeyRelatedField(queryset=Hotel.objects.all(), source='hotel', write_only=True)  # To allow setting hotel by ID

    class Meta:
        model = Review
        fields = ['id', 'user', 'user_id', 'hotel', 'hotel_id', 'rating', 'title', 'content', 'created_at', 'updated_at']
