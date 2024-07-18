from django.urls import path
from .views import add_webinar

urlpatterns = [
    path('add-webinar/', add_webinar),
]
