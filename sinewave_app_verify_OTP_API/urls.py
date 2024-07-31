from django.urls import path
from .views import VerifyOTPAPI

urlpatterns = [
    
    path('verify-otp/', VerifyOTPAPI.as_view(), name='verify-otp'),

]