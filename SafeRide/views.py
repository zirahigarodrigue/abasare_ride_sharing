from django.shortcuts import render
from rest_framework import generics, mixins, viewsets
from rest_framework.response import Response
from . models import *
from .serializers import *
from .models import Task




class UmusareRiderView(mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       viewsets.GenericViewSet):
    serializer_class = UmusareRiderSerializer

    def get_queryset(self):
        queryset = UmusareRider.objects.all()
        user_id = self.kwargs.get('user_id')
        rider_id = self.kwargs.get('rider_id')

        if user_id:
            queryset= queryset.filter(user__id = user_id)
        elif user_id and rider_id:
            queryset= queryset.filter(user__id = user_id,
                                      id = rider_id)
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer =self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer =self.get_serializer(instance)
        return Response(serializer.data)


class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class JourneyListCreateView(generics.ListCreateAPIView):
    queryset = Journey.objects.all()
    serializer_class = JourneySerializer

class ServicesListCreateView(generics.ListCreateAPIView):
    queryset = Services.objects.all()
    serializer_class = ServicesSerializer

class UmusareWageView(generics.ListCreateAPIView):
    queryset = UmusareWage.objects.all()
    serializer_class = UmusareWageSerializer


class ClientsView(mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       viewsets.GenericViewSet):
    serializer_class = ClientsSerializer

    def get_queryset(self):
        queryset = Clients.objects.all()
        user_id = self.kwargs.get('user_id')
        client_id = self.kwargs.get('client_id')

        if user_id and client_id:
            queryset= queryset.filter(user__id = user_id,
                                      id = client_id)
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer =self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer =self.get_serializer(instance)
        return Response(serializer.data)


class ClientPropertyView(viewsets.ModelViewSet):
    serializer_class = ClientPropertySerializer

    def get_queryset(self):
        queryset = ClientProperty.objects.all()
        user_id = self.kwargs.get('user_id')
        client_id = self.kwargs.get('client_id')
        vehicle_id = self.kwargs.get('vehicle_id')

        if vehicle_id and user_id and client_id:
            queryset= queryset.filter(client__user__id = user_id,
                                      client = client_id,
                                      id=vehicle_id)
        return queryset


class ClientRequestListCreateView(mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       viewsets.GenericViewSet):
    queryset = ClientRequest.objects.all()
    serializer_class = ClientRequestSerializer



