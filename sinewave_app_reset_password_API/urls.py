from django.urls import path
from .views import ResetPasswordAPI

urlpatterns = [

    path('reset-password/', ResetPasswordAPI.as_view(), name='reset-password'),
]