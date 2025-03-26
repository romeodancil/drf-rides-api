from rest_framework import serializers
from .userSerializers import UserSerializer
from manageRide.models import UserModel, RideModel, RideEventModel
from datetime import timedelta
from django.utils.timezone import now

class RidesEventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideEventModel
        fields = ["id_ride_event", "id_ride", "description", "created_at"]
class RideSerializer(serializers.ModelSerializer):
    id_rider = UserSerializer(read_only=True)
    id_driver = UserSerializer(read_only=True)
    ride_event = RidesEventsSerializer(many=True, read_only=True)
    todays_ride_events = serializers.SerializerMethodField()

    class Meta:
        model = RideModel
        fields = [
            'id_ride',
            'status', 
            'id_rider',
            'id_driver',
            'pickup_latitude', 
            'pickup_longitude',
            'dropoff_latitude',
            'dropoff_longitude',
            'pickup_time',
            'ride_event',
            'todays_ride_events',
        ]
    
    def get_todays_ride_events(self, obj):
        last_24_hours = now() - timedelta(hours=24)
        recent_events = obj.ride_event.filter(created_at__gte=last_24_hours)
        return RidesEventsSerializer(recent_events, many=True).data


class RideCreateSerializer(serializers.ModelSerializer):
    id_rider = serializers.PrimaryKeyRelatedField(queryset=UserModel.objects.all())
    id_driver = serializers.PrimaryKeyRelatedField(queryset=UserModel.objects.all(), required=False)

    class Meta:
        model = RideModel
        fields = [
            'id_ride',
            'status', 
            'id_rider',
            'id_driver',
            'pickup_latitude', 
            'pickup_longitude',
            'dropoff_latitude',
            'dropoff_longitude',
            'pickup_time'
        ]

        def create(self, validated_data):
            return RideModel.objects.create(**validated_data)

class RideUpdateSerializer(serializers.ModelSerializer):
    id_driver = serializers.PrimaryKeyRelatedField(
        queryset=UserModel.objects.all(), required=False
    )
    pickup_time = serializers.DateTimeField(required=False)

    class Meta:
        model = RideModel
        fields = ["id_driver", "pickup_time"]

    def update(self, instance, validated_data):
        instance.id_driver = validated_data.get("id_driver", instance.id_driver)
        instance.pickup_time = validated_data.get("pickup_time", instance.pickup_time)
        instance.save()
        return instance


class RidesEventsCreateSerializer(serializers.ModelSerializer):
    id_ride = serializers.PrimaryKeyRelatedField(
        queryset=RideModel.objects.all(), required=False
    )
    class Meta:
        model = RideEventModel
        fields = ["id_ride_event", "id_ride", "description", "created_at"]

    def create(self, validated_data):
        return RideEventModel.objects.create(**validated_data)