from django.urls import path
from .views import CustomerRegistration, CustomerLogin, CustomerLogout

urlpatterns = [
    path('register/', CustomerRegistration.as_view(), name='customer-registration'),
    path('login/', CustomerLogin.as_view(), name='customer-login'),
    path('logout/', CustomerLogout.as_view(), name='customer-logout'),
]
