from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlaceViewSet, HotelViewSet, ReviewViewSet, UserProfileView

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'places', PlaceViewSet)
router.register(r'hotels', HotelViewSet)
router.register(r'reviews', ReviewViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),  # Include the router URLs
    path('user-profile/', UserProfileView.as_view(), name='user-profile'),
]
