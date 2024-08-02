from django.urls import path
from .views import get_request_types

urlpatterns = [
    path('get-request-types/', get_request_types),
]
