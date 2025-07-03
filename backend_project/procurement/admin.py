from django.contrib import admin

# Register your models here.
from .models import Request, PurchaseOrder

# Register your models to appear in the Django admin panel
admin.site.register(Request)
admin.site.register(PurchaseOrder)
