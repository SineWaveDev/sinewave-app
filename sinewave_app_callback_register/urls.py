from django.urls import path
from .views import insert_ticket

urlpatterns = [
    path('insert-ticket/', insert_ticket, name='insert_ticket'),
]
