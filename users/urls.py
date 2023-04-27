from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet, UserRegisterView, LoginView, LogoutView, AccountActivationView


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'login/', LoginView.as_view(), name='login'),
    path(r'register/', UserRegisterView.as_view(), name='register'),
    path(r'activate-account/<uidb64>/<token>/', AccountActivationView.as_view(), name='activation'),
    path(r'logout/', LogoutView.as_view(), name='logout'),
    #path(r'resetpassword/', ResetPasswordView.as_view(), name='reset'),
]
