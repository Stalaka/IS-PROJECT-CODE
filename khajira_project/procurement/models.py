from django.db import models

# Create your models here.
from django.contrib.auth.models import User
class Request(models.Model):
    REQUEST_STATUS = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    item_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    requester = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=REQUEST_STATUS, default='pending')
    date_requested = models.DateField(auto_now_add=True)

    def _str_(self):
        return f"{self.item_name} - {self.status}"


class PurchaseOrder(models.Model):
    ORDER_STATUS = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('shipped', 'Shipped'),
    ]

    item_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    supplier = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=ORDER_STATUS, default='pending')
    order_date = models.DateField(auto_now_add=True)

    def _str_(self):
        return f"{self.item_name} ({self.status})"


