"""
URL configuration for sinewave_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


urlpatterns = [
    path('api/', include('sinewave_APP_API.urls')),
    path('api/', include('sinewave_app_callback_register.urls')),
    path('api/', include('sinewave_update_profile_api.urls')),
    path('api/', include('sinewave_app_webinar_registration_api.urls')),
    path('api/', include('sinewave_app_product_list_api.urls')),
    path('api/', include('sinewave_app_get_profile_details.urls')),
    path('api/', include('sinewave_all_grt_Cust_AUC_and_Product_Details.urls')),
    path('api/', include('webinar_data.urls')),
    path('api/', include('sinewave_app_request_OTP_API.urls')),
    path('api/', include('sinewave_app_reset_password_API.urls')),
    path('api/', include('sinewave_app_verify_OTP_API.urls')),
    path('api/', include('request_type.urls')),
    path('api/', include('Payment_History_API.urls')),
    path('api/', include('Coin_Rewards_System.urls')),
    path('api/', include('teams_calling_system.urls')),
    
    
    
    
    
]
