from django.urls import path
from . import views

urlpatterns = [
    path('user/login/', views.user_login, name='user_login'),
    path('user/update_coins/', views.update_coins, name='update_coins'),
    path('user/balance/<str:user_id>/', views.get_user_balance, name='get_user_balance'),
    path('user/log_transaction/<str:user_id>/', views.log_transaction, name='log_transaction'),
    
]
