from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Request(models.Model):
    """Model to represent material requests made by system users."""

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

    def __str__(self):
        return f"{self.item_name} ({self.status})"

    class Meta:
        verbose_name = "Material Request"
        verbose_name_plural = "Material Requests"


class PurchaseOrder(models.Model):
    """Model to represent purchase orders sent to suppliers."""

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

    def __str__(self):
        return f"{self.item_name} ({self.status})"

    class Meta:
        verbose_name = "Purchase Order"
        verbose_name_plural = "Purchase Orders"
