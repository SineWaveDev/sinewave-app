from django.urls import path
from .views import get_customer_data

urlpatterns = [
    path('auc-data/<str:cust_id>/', get_customer_data, name='get_customer_data'),
]
