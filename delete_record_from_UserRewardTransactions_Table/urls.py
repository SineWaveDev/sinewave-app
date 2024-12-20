from django.urls import path
from .views import delete_user_reward_transaction

urlpatterns = [
    path('delete_user_reward_transaction/', delete_user_reward_transaction, name='delete_user_reward_transaction'),
]
