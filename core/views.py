from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, AllowAny
from .models import Place, Hotel, Review, User
from .serializers import PlaceSerializer, HotelSerializer, ReviewSerializer, UserSerializer
from .permissions import IsOwnerOrAdmin,IsSelfOrAdmin  # Import custom permission

class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ['name', 'country']
    permission_classes = [IsAuthenticatedOrReadOnly]  # Allow unauthenticated users to read

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [AllowAny]
        return super().get_permissions()


class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ['name', 'place','rating']
    permission_classes = [IsAuthenticatedOrReadOnly]  # Allow unauthenticated users to read

    def get_permissions(self):
        if self.action in ['create', 'update','partial_update','destroy']:
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [AllowAny]
        return super().get_permissions()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsSelfOrAdmin]
        else:
            self.permission_classes = [AllowAny]
        return super().get_permissions()

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.select_related('user','hotel').all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Allow unauthenticated users to read
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ['hotel']

    def perform_create(self, serializer):
        # Assign the user who created the review
        serializer.save(user=self.request.user)

    def get_permissions(self):
        # Custom permissions for update and delete actions
        if self.action in ['update','partial_update','destroy']:
            self.permission_classes = [IsOwnerOrAdmin]
        elif self.action == 'create':
            self.permission_classes = [IsAuthenticatedOrReadOnly]
        else:
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def get_queryset(self):
        # Optionally filter reviews by hotel if needed
        hotel_id = self.request.query_params.get('hotel_id', None)
        if hotel_id is not None:
            return self.queryset.filter(hotel_id=hotel_id)
        return self.queryset
