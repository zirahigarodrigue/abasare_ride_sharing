from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from rest_framework import status, viewsets, mixins, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

import jwt
from datetime import datetime, timedelta
from .serializers import UserSerializer, LoginSerializer, PasswordResetSerializer, PasswordResetConfirmSerializer, LogoutSerializer

User = get_user_model()


class RegistrationView(generics.GenericAPIView):
    serializer_class = UserSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user_email = serializer.validated_data['email']
            if User.objects.filter(email=user_email).exists():
                return Response({"message": "This email is already registered."}, status=status.HTTP_400_BAD_REQUEST)

            user = serializer.save()
            user.is_active = False
            user.save()

            # Send email with activation link
            activation_link = reverse('user-activate', kwargs={
                'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            activation_url = request.build_absolute_uri(activation_link)
            message = EmailMessage(
                subject='Activate your account',
                body=f'Please click on this link to activate your account: {activation_url}',
                to=[user.email],
            )
            message.send()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivateView(APIView):
    """API view to activate a user's account"""
    def get(self, request, uidb64, token):
        """Verify the activation token and activate the user's account"""
        try:
            uid = str(urlsafe_base64_decode(uidb64), encoding='utf-8')
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({'message': 'Your account has been activated successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid activation link.'}, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = get_object_or_404(User, email=email)

            # Generate token and URL for password reset
            token = default_token_generator.make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            password_reset_link = reverse('password-reset-confirm', kwargs={
                'uidb64': uidb64,
                'token': token,
            })
            password_reset_url = request.build_absolute_uri(password_reset_link)

            # Send email with password reset link
            message = EmailMessage(
                subject='Password Reset Requested',
                body=f'Please click on this link to reset your password: {password_reset_url}',
                to=[email],
            )
            message.send()

            return Response({'message': 'Password reset link has been sent to your email address.'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, uidb64, token):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                uid = urlsafe_base64_decode(uidb64).decode()
                user = User.objects.get(pk=uid)
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                user = None

            if user is not None and default_token_generator.check_token(user, token):
                form = SetPasswordForm(user, request.data)
                if form.is_valid():
                    form.save()
                    return Response({"message": "Your password has been reset successfully."}, status=status.HTTP_200_OK)
                else:
                    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "Password reset link is invalid."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                request,
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password']
            )
            if user is not None:
                login(request, user)
                serializer = UserSerializer(user)
                # Create JWT token
                payload = {
                    'user_id': user.pk,
                    'exp': datetime.utcnow() + timedelta(days=1),
                    'iat': datetime.utcnow(),
                }
                token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
                response = Response({'message': 'Login successful.'}, status=status.HTTP_200_OK)
                response.set_cookie(key='jwt', value=token, httponly=True)
                response.data = {
                    'token': token,
                    'user': serializer.data,
                }
                return response
            else:
                return Response({'message': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserView(mixins.ListModelMixin, 
                  mixins.UpdateModelMixin, 
                  mixins.DestroyModelMixin, 
                  viewsets.GenericViewSet):
    # authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self):
        token = self.request.COOKIES.get('jwt')
        if not token:
            return Response({'error': 'Unauthorized.'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            # Decode JWT token
            token = self.request.COOKIES.get('jwt')
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Unauthorized.'}, status=status.HTTP_401_UNAUTHORIZED)

        # Get user_id from the JWT token
        user_id = decoded_token['user_id']

        # Get user object from the user_id
        user = self.queryset.filter(pk=user_id).first()

        if not user:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        if not user.is_active:
            return Response({'error': 'User account is not active.'}, status=status.HTTP_401_UNAUTHORIZED)
        return user

    def list(self, request):
        user = self.get_object()
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        user = self.get_object()
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def update(self, request, pk=None):
        user = self.get_object()
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        user = self.get_object()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]
    def post(self, request):
        logout(request)
        response = Response({"success": "You are now logged out successfully."}, status=status.HTTP_200_OK)
        response.delete_cookie('jwt')
        return response
