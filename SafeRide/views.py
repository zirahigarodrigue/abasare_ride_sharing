from django.shortcuts import render
from rest_framework import generics
from . models import *
from .serializers import *
from .models import Task




class UmusareRiderListCreateView(generics.ListCreateAPIView):
    queryset = UmusareRider.objects.all()
    serializer_class = UmusareRiderSerializer

class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class JourneyListCreateView(generics.ListCreateAPIView):
    queryset = Journey.objects.all()
    serializer_class = JourneySerializer

class ServicesListCreateView(generics.ListCreateAPIView):
    queryset = Services.objects.all()
    serializer_class = ServicesSerializer

class UmusareWageListCreateView(generics.ListCreateAPIView):
    queryset = UmusareWage.objects.all()
    serializer_class = UmusareWageSerializer


class ClientsListCreateView(generics.ListCreateAPIView):
    queryset = Clients.objects.all()
    serializer_class = ClientsSerializer
    
class ClientPropertyListCreateView(generics.ListCreateAPIView):
    queryset = ClientProperty.objects.all()
    serializer_class = ClientPropertySerializer


class ClientRequestListCreateView(generics.ListCreateAPIView):
    queryset = ClientRequest.objects.all()
    serializer_class = ClientRequestSerializer
