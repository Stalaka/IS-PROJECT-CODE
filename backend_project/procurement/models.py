from django.db import models
from django.contrib.auth.models import User

# --- Item Model (Tracks current rate) ---
class Item(models.Model):
    name = models.CharField(max_length=100, unique=True)
    current_rate = models.DecimalField(max_digits=10, decimal_places=2)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# --- Rate History (for item price change log) ---
class RateHistory(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    old_rate = models.DecimalField(max_digits=10, decimal_places=2)
    new_rate = models.DecimalField(max_digits=10, decimal_places=2)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item.name} changed on {self.changed_at.strftime('%Y-%m-%d')}"


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

    # ✅ Supplier field added back
    supplier = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    status = models.CharField(max_length=10, choices=ORDER_STATUS, default='pending')
    order_date = models.DateField(auto_now_add=True)
    purchase_document = models.FileField(upload_to='purchase_docs/', null=True, blank=True)

    def __str__(self):  
        return f"{self.item_name} ({self.status})"

    class Meta:
        verbose_name = "Purchase Order"
        verbose_name_plural = "Purchase Orders"


# --- Manufacturer Production Update ---
class ProductionUpdate(models.Model):
    COMPLETION_STATUS = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('delayed', 'Delayed'),
    ]

    order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    manufacturer = models.ForeignKey(User, on_delete=models.CASCADE)
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


# --- Audit Log Model (Tracks all critical user actions) ---
class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.timestamp.strftime('%Y-%m-%d %H:%M')} - {self.user} - {self.action}"
