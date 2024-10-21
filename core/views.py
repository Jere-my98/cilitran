from django.urls import reverse
from django.shortcuts import redirect
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status,viewsets, filters, generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, AllowAny, IsAuthenticated
from .models import Place, Hotel, Review, User
from .serializers import PlaceSerializer, HotelSerializer, ReviewSerializer, UserSerializer, UserProfileSerializer
from .permissions import IsOwnerOrAdmin,IsSelfOrAdmin  # Import custom permission

class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ['name', 'country']
    permission_classes = [IsAuthenticatedOrReadOnly]  # Default permission

    def get_permissions(self):
        """Set permissions based on the action being performed."""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]  # Only admins can create/update/delete
        else:
            self.permission_classes = [AllowAny]  # Anyone can read
        return super().get_permissions()
    
    def create(self, request, *args, **kwargs):
        """Handle the POST request to create a new place"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # Validate the request data
        self.perform_create(serializer)  # Save the new place instance

        place_id=serializer.data['id']
        place_detail_url=reverse('place-detail', args=[place_id])
        # headers = self.get_success_headers(serializer.data)  # Get headers for the response
        # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)  # Return the created place data
        return redirect(place_detail_url)
    
    def update(self, request, *args, **kwargs):
        """Handle the PUT request to update a place"""
        partial = kwargs.pop('partial', False)  # Determine if it's a partial or full update
        instance = self.get_object()  # Get the place instance to update
        serializer = self.get_serializer(instance, data=request.data, partial=partial)  # Bind the data to the serializer
        serializer.is_valid(raise_exception=True)  # Validate the data
        self.perform_update(serializer)  # Perform the update
        return Response(serializer.data, status=status.HTTP_200_OK)  # Return the updated place data

    def destroy(self, request, *args, **kwargs):
        """Handle the DELETE request to delete a place"""
        instance = self.get_object()  # Get the place instance to delete
        self.perform_destroy(instance)  # Perform the deletion
        return Response(status=status.HTTP_204_NO_CONTENT)  # Return empty response after successful deletion

class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ['name', 'place', 'rating']
    permission_classes = [IsAuthenticatedOrReadOnly]  # Default permission
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]  # Only admins can create/update/delete
        else:
            self.permission_classes = [AllowAny]  # Allow read for everyone
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        """Handle the POST request to create a new hotel"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # Validate the request data
        self.perform_create(serializer)  # Save the new hotel instance
        headers = self.get_success_headers(serializer.data)  # Get headers for the response
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)  # Return the created hotel data
    
    def update(self, request, *args, **kwargs):
        """Handle the PUT request to update a hotel"""
        partial = kwargs.pop('partial', False)  # Check if it's a full update or partial
        instance = self.get_object()  # Get the hotel instance
        serializer = self.get_serializer(instance, data=request.data, partial=partial)  # Bind data to the serializer
        serializer.is_valid(raise_exception=True)  # Validate the data
        self.perform_update(serializer)  # Save the updated instance

        return Response(serializer.data, status=status.HTTP_200_OK)  # Return the updated hotel data

    def destroy(self, request, *args, **kwargs):
        """Handle the DELETE request to delete a hotel"""
        instance = self.get_object()  # Get the hotel instance to delete
        self.perform_destroy(instance)  # Perform the deletion
        return Response(status=status.HTTP_204_NO_CONTENT)  # Return empty response with 204 status

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [IsAdminUser]  # Only admins can list all users
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsSelfOrAdmin]  # Admins and self can modify accounts
        else:
            self.permission_classes = [AllowAny]  # Anyone can register
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        """Allow anonymous users to register"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """Allow admins to update any user, users can update their own data"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """Allow admins to delete any user, users can delete their own accounts"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserProfileView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Return the current authenticated user
        return self.request.user

    def destroy(self, request, *args, **kwargs):
        """Allow users to delete their own account."""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.select_related('user', 'hotel').all()  # Optimize with select_related
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Default: allow reading to all
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ['hotel']

    def perform_create(self, serializer):
        """Assign the current authenticated user as the creator of the review"""
        serializer.save(user=self.request.user)

    def get_permissions(self):
        """Custom permissions based on actions"""
        if self.action in ['update', 'partial_update', 'destroy']:
            # Only allow the review owner or admin to update/delete
            self.permission_classes = [IsOwnerOrAdmin]
        elif self.action == 'create':
            # Only authenticated users can create reviews
            self.permission_classes = [IsAuthenticated]
        else:
            # Allow all users (even anonymous) to read reviews
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def get_queryset(self):
        """
        Optimize the query by reducing redundant queries.
        - Admins: See all reviews.
        - Authenticated users: Can see their own reviews globally and all reviews for a specific hotel.
        - Anonymous users: Can only list reviews for a specific hotel.
        """
        user = self.request.user
        hotel_id = self.request.query_params.get('hotel_id', None)

        # Admins can access all reviews
        if user.is_staff:
            # Prefetch related data for hotel and user for performance
            return self.queryset

        # Authenticated users can view their own reviews or all reviews for a specific hotel
        if user.is_authenticated:
            if hotel_id:
                # List all reviews for a specific hotel, regardless of the author
                return self.queryset.filter(hotel_id=hotel_id).select_related('user', 'hotel')
            else:
                # List only the user's own reviews across all hotels
                return self.queryset.filter(user=user).select_related('user', 'hotel')

        # Anonymous users can only see reviews for a specific hotel
        if hotel_id:
            return self.queryset.filter(hotel_id=hotel_id).select_related('user', 'hotel')

        # Anonymous users cannot access any other reviews globally
        return self.queryset.none()

