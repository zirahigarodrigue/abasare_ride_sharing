from django.urls import path, include
# from rest_framework import routers
from rest_framework_nested import routers

from SafeRide.views import (
    UmusareRiderView,
    ClientsView,
    ClientPropertyView
)

from .views import (
    RegistrationView,
    ActivateView,
    PasswordResetView,
    PasswordResetConfirmView,
    LoginView,
    UserView,
    LogoutView,
)

router = routers.DefaultRouter()
router.register(r'users', UserView, basename='user')

profile_router = routers.NestedSimpleRouter(router, r'users', lookup='user')
profile_router.register(r'umusare', UmusareRiderView, basename='umusare')
profile_router.register(r'client', ClientsView, basename='client')

property_router = routers.NestedSimpleRouter(profile_router, r'client', lookup='client')
property_router.register(r'vehicles', ClientPropertyView, basename='vehicle')

# property_router = routers.NestedSimpleRouter(profile_router, r'umusare', lookup='umusare')
# property_router.register(r'vehicles', ClientPropertyView, basename='vehicle')

urlpatterns = [
    path(r'', include(router.urls)),
    path('', include(profile_router.urls)),
    path('', include(property_router.urls)),
    path(r'register/', RegistrationView.as_view(), name='user-register'),
    path(r'activate/<uidb64>/<token>/', ActivateView.as_view(), name='user-activate'),
    path(r'login/', LoginView.as_view(), name='user-login'),
    path(r'logout/', LogoutView.as_view(), name='user-logout'),
    path(r'password_reset/', PasswordResetView.as_view(), name='password-reset'),
    path(r'password/reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
]