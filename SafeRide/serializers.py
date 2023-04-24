from rest_framework import serializers
from .models import *

class UmusareRiderSerializer(serializers.ModelSerializer):
    class Meta:
        model = UmusareRider
        fields = '__all__'

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

class UmusareWageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UmusareWage
        fields = '__all__'        

class ClientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clients
        fields = '__all__'

class ClientPropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientProperty
        fields = '__all__'


class ClientRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientRequest
        fields = '__all__'
