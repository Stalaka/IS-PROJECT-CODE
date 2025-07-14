from django.contrib import admin
from .models import Request, PurchaseOrder, ProductionUpdate, Item, RateHistory, Vendor

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'quantity', 'status', 'requester', 'date_requested')
    list_filter = ('status', 'date_requested')
    search_fields = ('item_name', 'requester__username')

@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'quantity', 'supplier', 'status', 'order_date', 'purchase_document')
    list_filter = ('status', 'order_date', 'supplier')
    search_fields = ('item_name', 'supplier__name')

@admin.register(ProductionUpdate)
class ProductionUpdateAdmin(admin.ModelAdmin):
    list_display = (
        'order',
        'manufacturer',
        'start_date',
        'end_date',
        'production_deadline',
        'completion_status',
        'is_completed',
        'updated_at'
    )
    list_filter = ('completion_status', 'production_deadline', 'is_completed')
    search_fields = ('order__item_name', 'manufacturer__username')

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'current_rate', 'updated_at')
    search_fields = ('name',)

@admin.register(RateHistory)
class RateHistoryAdmin(admin.ModelAdmin):
    list_display = ('item', 'old_rate', 'new_rate', 'changed_by', 'changed_at')
    list_filter = ('changed_at', 'changed_by')
    readonly_fields = ('changed_at',)

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    search_fields = ('name',)
    list_filter = ('is_active',)




