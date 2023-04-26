from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet, UserRegisterView, LoginView, LogoutView


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'login/', LoginView.as_view(), name='login'),
    path(r'register/', UserRegisterView.as_view(), name='register'),
    path(r'logout/', LogoutView.as_view(), name='logout'),
]