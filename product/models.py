from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime


user = get_user_model()

class Product(models.Model):
    name = models.CharField(max_length=100,unique=True)
    price = models.PositiveIntegerField()
    description = models.TextField()
    created_by = models.ForeignKey(user,related_name="products",on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"product {self.name} created by {self.created_by}"