from rest_framework import (
    viewsets,
    views,
    permissions,
    status
)
from .models import RideModel, UserModel, RideEventModel
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from manageRide.serializers import (
    RideSerializer,
    RideUpdateSerializer,
    RidesEventsSerializer,
    RideCreateSerializer,
    RidesEventsCreateSerializer
)
from .permissions import IsAdminUserRole
from rest_framework.generics import ListAPIView
from manageRide.ridesPagination import RidesPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Prefetch
from datetime import timedelta
from django.utils.timezone import now

class RidesView(views.APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUserRole]
    
    filter_backends = [DjangoFilterBackend]
    ordering_fields = ["-pickup_time"]
    ordering = ["-pickup_time"]

    def get_queryset(self):
        last_24_hours = now() - timedelta(hours=24)
    
        queryset = (
            RideModel.objects
            .select_related("id_rider", "id_driver") # Optimizes ForeignKey joins
            .order_by("pickup_time")
        )

        rider_email = self.request.query_params.get("rider_email", None)
        driver_email = self.request.query_params.get("driver_email", None)
        status = self.request.query_params.get("status", None)

        if rider_email:
            queryset = queryset.filter(id_rider__email=rider_email)
        if driver_email:
            queryset = queryset.filter(id_driver__email=driver_email)
        if status:
            queryset = queryset.filter(status=status)
        
        # Prefetch only recent RideEvents (Last 24 Hours)
        recent_events = RideEventModel.objects.filter(created_at__gte=last_24_hours)
        prefetch_recent_events = Prefetch("ride_event", queryset=recent_events)

        return queryset.prefetch_related(prefetch_recent_events).order_by("-pickup_time")

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginator = RidesPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        user_serializers = RideSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(user_serializers.data)

    def post(self, request, format=None):
        ride_serializers = RideCreateSerializer(data=request.data)
        if ride_serializers.is_valid():
            ride_serializers.save()
            return Response(ride_serializers.data, status=status.HTTP_200_OK)
        return Response(ride_serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        try:
            ride_id = request.data.get('ride_id')
            ride = RideModel.objects.get(id_ride=ride_id)
        except RideModel.DoesNotExist:
            return Response({"error": "Ride not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = RideUpdateSerializer(ride, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RidesEvents(views.APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUserRole]

    def get(self, request, format=None):
        user_serializers = RidesEventsSerializer(RideEventModel.objects.all(), many=True)
        return Response(user_serializers.data)

    def post(self, request, format=None):
        ride_events_serializers = RidesEventsCreateSerializer(data=request.data)
        if ride_events_serializers.is_valid():
            ride_events_serializers.save()
            return Response(ride_events_serializers.data, status=status.HTTP_200_OK)
        return Response(ride_events_serializers.errors, status=status.HTTP_400_BAD_REQUEST)