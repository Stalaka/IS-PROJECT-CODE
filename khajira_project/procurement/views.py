from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

from django.shortcuts import render
from .models import Request, PurchaseOrder

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
#Request form & Purchase Order Form
from .forms import RequestForm, PurchaseOrderForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

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
#Approved request
def approved_requests(request):
    data = Request.objects.filter(status='approved')
    return render(request, 'approved_requests.html', {'data': data})
