from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.forms import SetPasswordForm


from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

import jwt
# import datetime import datetime

from .serializers import UserSerializer, LoginSerializer

User = get_user_model()

# Create your views here.
class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid:
            user_email = serializer.validated_data['email']
            if User.objects.filter(email=user_email).exists():
                return Response({"message": "Email already exist."}, status=status.HTTP_400_BAD_REQUEST)
            user =serializer.save()
            user.save()
            return Response({"message": "Your account has been created successfully."}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer
        if serializer.is_valid():
            user=authenticate(
                request,
                email = serializer.validated_data['email'],
                password = serializer.validated_data['password']
            )
            if user is not None:
                login(request, user)
                serializ = UserSerializer(user)
                # create jwt
                payload = {
                    'user_id': user.pk,
                    'exp': datetime.utcnow() + timedelta(days=1),
                    'iat': datetime.utcnow(),
                }
                token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
                response = Response({"message": "Login successful."}, status=status.HTTP_200_OK)
                response.set_cookie(key='jwt', value=token, httponly=True)
                response.data={
                    'token': token,
                    'user': serializer.data,
                }
                return response
            else:
                return Response({"message": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        response = Response({"success": "User logged out successfully."}, status=status.HTTP_200_OK)
        response.delete_cookie('jwt')
        return response

class UserViewSet(mixins.ListModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes=[IsAuthenticated]

    def get_object(self):
        token = self.request.COOKIES.get('jwt')
        if not token:
            return Response({"error": "Unauthorized."}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            token =self.request.COOKIES.get('jwt')
            decode_token = jwt.decode(token, settings.SECRET_KEY,algorithms='HS256')
        except jwt.ExpiredSignatureError:
            return Response({"error": "Unauthorized."}, status=status.HTTP_401_UNAUTHORIZED)
        userid =decode_token['user_id']
        user=self.queryset.filter(pk=userid).first()

        if not user:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return user
    
    def list(self, request):
        user= self.get_object()
        serializer=UserSerializer(user)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        user= self.get_object()
        serializer=UserSerializer(user)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        user= self.get_object()
        serializer=UserSerializer(user, data=request.data)
        if serializer.is_valid:
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request):
        user= self.get_object()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
