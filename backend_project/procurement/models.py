from django.db import models
from django.contrib.auth.models import User

# --- Material Request Model ---
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

    def __str__(self):
        return f"{self.item_name} ({self.status})"

    class Meta:
        verbose_name = "Material Request"
        verbose_name_plural = "Material Requests"


# --- Purchase Order Model ---
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

    def __str__(self):
        return f"{self.item_name} ({self.status})"

    class Meta:
        verbose_name = "Purchase Order"
        verbose_name_plural = "Purchase Orders"


# --- Manufacturer Production Update Model ---
class ProductionUpdate(models.Model):
    COMPLETION_STATUS = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('delayed', 'Delayed'),
    ]

    order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    manufacturer = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Additional timeline fields
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)

    production_deadline = models.DateField()
    completion_status = models.CharField(max_length=20, choices=COMPLETION_STATUS)
    notes = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Production update for Order #{self.order.id}"

    class Meta:
        verbose_name = "Production Update"
        verbose_name_plural = "Production Updates"

