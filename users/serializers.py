from django.urls import reverse
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError, force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True
    )
    password_confirm = serializers.CharField(
        max_length=68, min_length=6, write_only=True
    )
    token = serializers.CharField(max_length=500, read_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'password_confirm', 'is_vehicle_owner', 'is_umusare_rider', 'token']

    def validate(self, attrs):
        email = attrs.get('email', '')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': 'Email is already in use'})
        password = attrs.get('password', '')
        password_confirm = attrs.get('password_confirm', '')
        if password != password_confirm:
            raise serializers.ValidationError({'password': 'Passwords do not match'})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.context['request']).domain
        uidb64 = urlsafe_base64_encode(smart_bytes(user.pk))
        token = PasswordResetTokenGenerator().make_token(user)
        activation_link = reverse('activation', kwargs={'uidb64': uidb64, 'token': token})
        activate_url = 'http://' + current_site + activation_link

        message = EmailMessage(
            subject='Activate your account',
            body =f'Please click here on this link to activate your account: {activate_url}',
            to=[user.email]
        )
        message.send()
        return Response(serializers.data)

class AccountActivationSerializer(serializers.Serializer):
    token = serializers.CharField()
    uidb64 = serializers.CharField()

    def validate(self, attrs):
        try:
            uid = urlsafe_base64_decode(attrs['uidb64'])
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise ValidationError({'error': 'Invalid activation link'})

        if PasswordResetTokenGenerator().check_token(user, attrs['token']):
            user.is_active = True
            user.save()
            return attrs
        else:
            raise ValidationError({'error': 'Invalid activation link'})


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'is_vehicle_owner', 'is_umusare_rider')
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password is not None:
            user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class LoginSerializer(serializers.Serializer):
    email =serializers.EmailField()
    password =serializers.CharField(write_only=True)


class LogoutSerializer(serializers.Serializer):
    pass