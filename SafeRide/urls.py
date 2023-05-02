from django.urls import path, include
from rest_framework import routers 
from django.urls import path
from .views import TaskListCreateView, JourneyListCreateView, ServicesListCreateView, ClientRequestListCreateView 

urlpatterns = [
    path('Task/', TaskListCreateView.as_view(), name='Task'),
    path('journey/', JourneyListCreateView.as_view(), name='journey'),
    path('Services/', ServicesListCreateView.as_view(), name='Services'),
    path('ClientRequest/', ClientRequestListCreateView.as_view(), name='ClientRequest'),
    
]