# In your urls.py
from django.urls import path
from .views import DeleteLoginCountAPI

urlpatterns = [
    path('delete-login-count/<int:cust_id>/', DeleteLoginCountAPI.as_view(), name='delete-login-count'),
]