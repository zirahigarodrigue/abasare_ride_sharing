from datetime import datetime, timedelta
from django.conf import settings
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.forms import SetPasswordForm


from rest_framework import viewsets, mixins, status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

import jwt
# import datetime import datetime

from .serializers import UserSerializer, LoginSerializer, LogoutSerializer, RegisterSerializer, AccountActivationSerializer

User = get_user_model()

# Create your views here.
class UserRegisterView(generics.CreateAPIView):
    """
    View to handle user registration
    """
    serializer_class = RegisterSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False
            user.save()
            
            # Send activation email
            activation_url = reverse('activate-account')
            activation_url += f'?token={user.generate_activation_token()}'
            activation_link = f"{settings.BASE_URL}{activation_url}"
            send_mail(
                'Activate Your Account',
                f'Click on the link to activate your account: {activation_link}',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountActivationView(APIView):
    serializer_class = AccountActivationSerializer
    def post(self, request, uidb64, token):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'success': 'Account activation successful.'}, status=status.HTTP_200_OK)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    # permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            request,
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )
        if user:
            login(request, user)
            payload = {
                'user_id': user.pk,
                'exp': datetime.utcnow() + timedelta(days=1),
                'iat': datetime.utcnow(),
            }
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
            response = Response({"message": "Login successful."}, status=status.HTTP_200_OK)
            response.set_cookie(key='jwt', value=token, httponly=True)
            response.data = {
                'token': token,
            }
            return response
        else:
            return Response({"message": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
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
    
class ResetPasswordView(APIView):
    def post(self, request):
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()
        if not user:
            return Response({"message": "No user found with that email."}, status=status.HTTP_404_NOT_FOUND)
        # generate reset password token
        payload = {
            'user_id': user.pk,
            'exp': datetime.utcnow() + timedelta(hours=1),
            'iat': datetime.utcnow(),
            'type': 'reset_password'
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        # send email to user with reset password link
        # ...
        return Response({"message": "Password reset email sent."}, status=status.HTTP_200_OK)

class ConfirmResetPasswordView(APIView):
    def post(self, request):
        token = request.data.get('token')
        password = request.data.get('password')
        try:
            decode_token = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            if decode_token['type'] != 'reset_password':
                return Response({"error": "Invalid token type."}, status=status.HTTP_400_BAD_REQUEST)
            user_id = decode_token['user_id']
            user = User.objects.filter(pk=user_id).first()
            if not user:
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
            form = SetPasswordForm(user, {'new_password1': password, 'new_password2': password})
            if form.is_valid():
                form.save()
                return Response({"message": "Password reset successfully."}, status=status.HTTP_200_OK)
            else:
                return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
        except jwt.ExpiredSignatureError:
            return Response({"error": "Token expired."}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.DecodeError:
            return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)
