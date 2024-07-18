from django.urls import path
from .views import check_credentials


urlpatterns = [
    path('login/', check_credentials, name='login'),
]



