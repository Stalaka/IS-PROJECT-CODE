from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Request, PurchaseOrder

@login_required
def dashboard(request):
    total_requests = Request.objects.count()
    approved_requests = Request.objects.filter(status='approved').count()
    pending_requests = Request.objects.filter(status='pending').count()
    purchase_orders = PurchaseOrder.objects.count()

    # Temporary hardcoded notifications 
    notifications = [
        "✅ Order #002 has been approved",
        "⚠️ Low stock alert: Passport Paper",
        "📩 New request submitted by Felista",
        "📦 Delivery confirmation from GlobalPrint Ltd",
    ]

    return render(request, 'procurement.html', {
        'total_requests': total_requests,
        'approved_requests': approved_requests,
        'pending_requests': pending_requests,
        'purchase_orders': purchase_orders,
        'notifications': notifications  
    })

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Request

@login_required
def request_list(request):
    requests = Request.objects.all()
    return render(request, 'requests.html', {'requests': requests})

from .models import PurchaseOrder  

@login_required
def purchase_order_list(request):
    orders = PurchaseOrder.objects.all()
    return render(request, 'purchase_orders.html', {'orders': orders})

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def account_list(request):
    return render(request, 'accounts.html')  

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def settings_page(request):
    return render(request, 'settings.html') 

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import RequestForm

@login_required
def new_request(request):
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            new = form.save(commit=False)
            new.requester = request.user
            new.save()
            return redirect('dashboard')
    else:
        form = RequestForm()
    return render(request, 'new_request.html', {'form': form})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PurchaseOrderForm

@login_required
def new_order(request):
    if request.method == 'POST':
        form = PurchaseOrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = PurchaseOrderForm()
    return render(request, 'new_order.html', {'form': form})

from django.contrib.auth.decorators import login_required
from .models import Request
from django.shortcuts import render

@login_required
def approved_requests(request):
    data = Request.objects.filter(status='approved')
    return render(request, 'approved_requests.html', {'data': data})
