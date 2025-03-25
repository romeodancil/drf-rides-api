from rest_framework import (
    viewsets,
    views,
    permissions,
    status
    
)
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from .serializers import UserSerializer
from .models import UserModel
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from .permissions import IsAdminUserRole

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_user_token(request):
    email = request.data.get('email')
    try:
        user = UserModel.objects.get(email=email)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    except UserModel.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)

class UserView(views.APIView):
    def get_authenticators(self):
        if self.request.method == 'GET':
            return [TokenAuthentication()]
        return []

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.AllowAny()]
        return [IsAdminUserRole()]

    def get(self, request, format=None):
        user_serializers = UserSerializer(UserModel.objects.all(), many=True)
        return Response(user_serializers.data)

    def post(self, request, format=None):
        user_serializers = UserSerializer(data=request.data)
        if user_serializers.is_valid():
            user_serializers.save()
            return Response(user_serializers.data, status=status.HTTP_200_OK)
        return Response(user_serializers.errors, status=status.HTTP_400_BAD_REQUEST)