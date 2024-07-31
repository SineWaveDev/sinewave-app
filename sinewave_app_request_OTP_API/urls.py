from django.urls import path
from .views import RequestOTPAPI

urlpatterns = [
    path('request-otp/', RequestOTPAPI.as_view(), name='request-otp'),
   
]