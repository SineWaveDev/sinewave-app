from django.urls import path
from .views import update_customer

urlpatterns = [
    path('update-customer/', update_customer),
]
