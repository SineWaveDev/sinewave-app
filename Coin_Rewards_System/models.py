from django.db import models

# User model definition
class User(models.Model):
    # Define the fields for the User model
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# RewardTransaction model definition
class RewardTransaction(models.Model):
    # Define fields related to transactions
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    reward_points = models.IntegerField()
    transaction_type = models.CharField(max_length=50, choices=[('earn', 'Earn'), ('redeem', 'Redeem')])
    transaction_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.transaction_type} - {self.reward_points} points for {self.user}"

# Any other models related to your app can be added below
