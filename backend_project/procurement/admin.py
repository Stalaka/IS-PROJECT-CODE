from django.contrib import admin
from .models import Request, PurchaseOrder

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'quantity', 'status', 'requester', 'date_requested')
    list_filter = ('status', 'date_requested')
    search_fields = ('item_name', 'requester__username')

@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'quantity', 'supplier', 'status', 'order_date')
    list_filter = ('status', 'order_date')
    search_fields = ('item_name', 'supplier')
