from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Place, Hotel, Review
from .serializers import PlaceSerializer, HotelSerializer, ReviewSerializer
from .permissions import IsReviewAuthor  # Import your custom permission

class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Allow unauthenticated users to read

class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Allow unauthenticated users to read

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Allow unauthenticated users to read

    def perform_create(self, serializer):
        # Assign the user who created the review
        serializer.save(user=self.request.user)

    def get_permissions(self):
        # Custom permissions for update and delete actions
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAuthenticated, IsReviewAuthor]  # Only authors can update or delete
        return super().get_permissions()

    def get_queryset(self):
        # Optionally filter reviews by hotel if needed
        hotel_id = self.request.query_params.get('hotel_id', None)
        if hotel_id is not None:
            return self.queryset.filter(hotel_id=hotel_id)
        return self.queryset
