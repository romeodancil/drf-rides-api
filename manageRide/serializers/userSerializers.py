from rest_framework import serializers
from manageRide.models import UserModel

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['id_user', 'role', 'first_name', 'last_name', 'email', 'phone_number']
    
    def create(self, validated_data):
        if validated_data['role'].lower() == 'admin':
            return UserModel.objects.create_superuser(
                email=validated_data['email'],
                first_name=validated_data.get('first_name', ''),
                last_name=validated_data.get('last_name', ''),
                phone_number=validated_data.get('phone_number', ''),
            )
        return UserModel.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone_number=validated_data.get('phone_number', ''),
        )