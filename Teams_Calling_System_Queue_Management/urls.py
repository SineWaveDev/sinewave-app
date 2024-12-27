from django.urls import path
from .views import CreateMeetingView

urlpatterns = [
    path('CreateMeetingView/', CreateMeetingView.as_view(), name='CreateMeetingView'),
    
]
