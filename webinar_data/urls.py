from django.urls import path
from .views import get_webinar_details

urlpatterns = [
    path('webinar-details/', get_webinar_details, name='webinar-details'),
]
