from datetime import datetime, timedelta
from django.contrib.auth import get_user_model, authenticate, password_validation
from django.conf import settings
from django.utils.translation import gettext_lazy as _

import jwt

from rest_framework import serializers

from SafeRide.serializers import UmusareRiderSerializer, ClientsSerializer

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    rider_profile = UmusareRiderSerializer(read_only=True)
    client_profile = ClientsSerializer(read_only=True)

    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password_confirmation = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name","email","is_vehicle_owner","is_umusare_rider","password","password_confirmation","rider_profile","client_profile",]
        extra_kwargs = {
            'password': {'write_only': True,'required': True},
            'password_confirmation': {'write_only': True,'required': True},
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(_("This email address is already in use."))
        return value

    def validate(self, data):
        if data['password'] != data.pop('password_confirmation'):
            raise serializers.ValidationError(_("The passwords do not match."))
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = self.Meta.model(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)

            if user:
                if not user.is_active:
                    raise serializers.ValidationError("User account is not active.")
            else:
                raise serializers.ValidationError("Unable to login with the given credentials.")
        else:
            raise serializers.ValidationError("Must provide email and password.")

        data['user'] = user
        return data


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid email address')

        if not user.is_active:
            raise serializers.ValidationError('User account is inactive')

        return value



class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)

    def validate(self, data):
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data


class LogoutSerializer(serializers.Serializer):
    pass