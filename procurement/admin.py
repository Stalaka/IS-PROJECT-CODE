from django.contrib import admin
from .models import (
    User,
    Supplier,
    Material,
    ItemRateHistory,
    ProcurementRequest,
    PurchaseOrder,
    Delivery,
    ProductionPlan,
    AuditLog
)

admin.site.register(User)
admin.site.register(Supplier)
admin.site.register(Material)
admin.site.register(ItemRateHistory)
admin.site.register(ProcurementRequest)
admin.site.register(PurchaseOrder)
admin.site.register(Delivery)
admin.site.register(ProductionPlan)
admin.site.register(AuditLog)
