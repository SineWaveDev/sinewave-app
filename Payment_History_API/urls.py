from django.urls import path
from .views import get_payment_details

urlpatterns = [
    path('payment-details/', get_payment_details, name='payment-details'),
]
