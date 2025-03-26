from rest_framework import (
    viewsets,
    views,
    permissions,
    status
    
)
from .models import RideModel, UserModel
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from .serializers import RideSerializer, RideUpdateSerializer
from .permissions import IsAdminUserRole

class RidesView(views.APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUserRole]

    def get(self, request, format=None):
        user_serializers = RideSerializer(RideModel.objects.all(), many=True)
        return Response(user_serializers.data)

    def post(self, request, format=None):
        ride_serializers = RideSerializer(data=request.data)
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