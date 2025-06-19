from django.db import models
from django.contrib.auth.models import AbstractUser

# 1. Custom User model with roles
class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('procurement_officer', 'Procurement Officer'),
        ('supplier', 'Supplier'),
        ('manufacturer', 'Manufacturer'),
    ]
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)

# 2. Supplier model
class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact_email = models.EmailField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

# 3. Material model
class Material(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    current_rate = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

# 4. Item Rate History
class ItemRateHistory(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    old_rate = models.DecimalField(max_digits=10, decimal_places=2)
    new_rate = models.DecimalField(max_digits=10, decimal_places=2)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    updated_at = models.DateTimeField(auto_now_add=True)

# 5. Procurement Request
class ProcurementRequest(models.Model):
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ])
    created_at = models.DateTimeField(auto_now_add=True)

# 6. Purchase Order
class PurchaseOrder(models.Model):
    request = models.ForeignKey(ProcurementRequest, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('rejected', 'Rejected')
    ])

# 7. Delivery
class Delivery(models.Model):
    order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    delivered_quantity = models.PositiveIntegerField()
    delivery_date = models.DateField()
    confirmation_received = models.BooleanField(default=False)

# 8. Production Plan
class ProductionPlan(models.Model):
    manufacturer = models.ForeignKey(User, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity_needed = models.PositiveIntegerField()
    start_date = models.DateField()
    completion_date = models.DateField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)

# 9. Audit Log
class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
