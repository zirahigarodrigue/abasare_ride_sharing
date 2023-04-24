from django.urls import path, include
from rest_framework import routers 
from django.urls import path
from .views import UmusareRiderListCreateView, TaskListCreateView, JourneyListCreateView, ServicesListCreateView, UmusareWageListCreateView,ClientsListCreateView,ClientPropertyListCreateView,ClientRequestListCreateView 

urlpatterns = [
    path('UmusareRider/', UmusareRiderListCreateView.as_view(), name='UmusareRider'),
    path('Task/', TaskListCreateView.as_view(), name='Task'),
    path('journey/', JourneyListCreateView.as_view(), name='journey'),
    path('Services/', ServicesListCreateView.as_view(), name='Services'),
    path('UmusareWage/', UmusareWageListCreateView.as_view(), name='UmusareWage'),
    path('Clients/', ClientsListCreateView.as_view(), name='Clients'),
    path('ClientProperty/', ClientPropertyListCreateView.as_view(), name='ClientProperty'),
    path('ClientRequest/', ClientRequestListCreateView.as_view(), name='ClientRequest'),
    
]