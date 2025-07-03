from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import ProcurementRequest, PurchaseOrder


admin.site.register(Request)
admin.site.register(PurchaseOrder)
