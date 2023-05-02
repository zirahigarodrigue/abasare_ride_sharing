from rest_framework import serializers
from .models import *

class UmusareWageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UmusareWage
        fields = '__all__'        

class UmusareRiderSerializer(serializers.ModelSerializer):
    parent_lookup_kwargs ={
        'user_id': 'user__id',
        'rider_id': 'rider__id',
    }
    wages = UmusareWageSerializer(read_only=True, many=True)
    class Meta:
        model = UmusareRider
        fields = ['id','user','phone_number','bank_account','driving_license_category','profile_image','driving_license','national_id','wages',]

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class JourneySerializer(serializers.ModelSerializer):
    class Meta:
        model = Journey
        fields = '__all__'

class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = '__all__'

class ClientPropertySerializer(serializers.ModelSerializer):
    parent_lookup_kwargs ={
        'user_id': 'user__id',
        'client_id': 'client__id',
        'vehicle_id': 'vehicle__id',
    }
    class Meta:
        model = ClientProperty
        fields = ['id', 'Client', 'plate_number', 'car_type']


class ClientsSerializer(serializers.HyperlinkedModelSerializer):
    parent_lookup_kwargs ={
        'user_id': 'user__id',
        'rider_id': 'rider__id',
    }
    user = serializers.StringRelatedField(read_only=True)
    client_vehicles = ClientPropertySerializer(read_only=True, many=True)
    class Meta:
        model = Clients
        fields = ['id','user','phone_number', 'client_vehicles']


class ClientRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientRequest
        fields = '__all__'
