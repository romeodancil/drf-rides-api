from rest_framework import serializers
from manageRide.models import UserModel, RideModel
from .userSerializers import UserSerializer

class RideSerializer(serializers.ModelSerializer):
    id_rider = UserSerializer(read_only=True)
    id_driver = UserSerializer(read_only=True)

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