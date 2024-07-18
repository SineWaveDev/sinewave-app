# urls.py
from django.urls import path
from .views import get_customer_details

urlpatterns = [
    path('customer-details/', get_customer_details, name='get_customer_details'),
]
