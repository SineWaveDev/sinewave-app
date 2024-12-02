from django.urls import path
from .views import ScheduleMeeting

urlpatterns = [
    path('schedule-meeting/', ScheduleMeeting.as_view(), name='schedule-meeting'),
    
]
