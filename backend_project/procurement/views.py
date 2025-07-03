from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Request, PurchaseOrder

@login_required
def dashboard(request):
    total_requests = Request.objects.count()
    approved_requests = Request.objects.filter(status='approved').count()
    pending_requests = Request.objects.filter(status='pending').count()
    purchase_orders = PurchaseOrder.objects.count()

    return render(request, 'dashboard.html', {
        'total_requests': total_requests,
        'approved_requests': approved_requests,
        'pending_requests': pending_requests,
        'purchase_orders': purchase_orders
    })
