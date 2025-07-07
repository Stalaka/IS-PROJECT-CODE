from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Request, PurchaseOrder, ProductionUpdate
from .forms import RequestForm, PurchaseOrderForm, ProductionUpdateForm
from .serializers import RequestSerializer


# --- Custom Login View ---
class CustomLoginView(LoginView):
    template_name = 'login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.method == "GET":
            messages.info(request, "You are already logged into the system.")
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.get_user()
        allowed_roles = ['Admin', 'ProcurementOfficer', 'Supplier', 'Manufacturer']
        if not user.groups.filter(name__in=allowed_roles).exists():
            messages.error(self.request, "Access denied. You are not authorized.")
            return redirect('login')
        return super().form_valid(form)

    def get_success_url(self):
        user = self.request.user
        if user.groups.filter(name='Admin').exists():
            return reverse_lazy('dashboard')
        elif user.groups.filter(name='ProcurementOfficer').exists():
            return reverse_lazy('request_list')
        elif user.groups.filter(name='Supplier').exists():
            return reverse_lazy('purchase_order_list')
        elif user.groups.filter(name='Manufacturer').exists():
            return reverse_lazy('manufacturer_dashboard')
        return reverse_lazy('dashboard')


# --- Manufacturer Dashboard View ---
@login_required
def manufacturer_dashboard(request):
    materials_needed = Request.objects.filter(status='approved')
    deliveries = PurchaseOrder.objects.all()
    updates = ProductionUpdate.objects.filter(manufacturer=request.user)

    return render(request, 'manufacturer_dashboard.html', {
        'materials_needed': materials_needed,
        'deliveries': deliveries,
        'updates': updates,
    })


# --- Manufacturer Production Update Submission View ---
@login_required
def update_production_status(request, order_id):
    if request.method == 'POST':
        deadline = request.POST.get('deadline')
        status = request.POST.get('status')

        order = get_object_or_404(PurchaseOrder, id=order_id)
        update, created = ProductionUpdate.objects.get_or_create(
            order=order,
            manufacturer=request.user
        )
        update.production_deadline = deadline
        update.completion_status = status
        update.save()

        messages.success(request, f"Production status for Order #{order_id} updated.")
    return redirect('manufacturer_dashboard')


# --- Form-Based Update View ---
@login_required
def update_production(request):
    if request.method == 'POST':
        form = ProductionUpdateForm(request.POST)
        if form.is_valid():
            update = form.save(commit=False)
            update.manufacturer = request.user
            update.save()
            messages.success(request, "Production update saved.")
            return redirect('manufacturer_dashboard')
    else:
        form = ProductionUpdateForm()

    return render(request, 'update_production.html', {'form': form})


# --- Dashboard View ---
@login_required
def dashboard(request):
    total_requests = Request.objects.count()
    approved_requests = Request.objects.filter(status='approved').count()
    pending_requests = Request.objects.filter(status='pending').count()
    purchase_orders = PurchaseOrder.objects.count()

    notifications = [
        " Order #002 has been approved",
        " Low stock alert: Passport Paper",
        "New request submitted by Felista",
        "Delivery confirmation from GlobalPrint Ltd",
    ]

    return render(request, 'procurement.html', {
        'total_requests': total_requests,
        'approved_requests': approved_requests,
        'pending_requests': pending_requests,
        'purchase_orders': purchase_orders,
        'notifications': notifications
    })


@login_required
def request_list(request):
    requests = Request.objects.all()
    return render(request, 'requests.html', {'requests': requests})


@login_required
def purchase_order_list(request):
    orders = PurchaseOrder.objects.all()
    return render(request, 'purchase_orders.html', {'orders': orders})


@login_required
def account_list(request):
    users = User.objects.all()
    return render(request, 'account.html', {'users': users})


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


@login_required
def approved_requests(request):
    data = Request.objects.filter(status='approved')
    return render(request, 'approved_requests.html', {'data': data})


# --- API Endpoint: List all procurement requests ---
@api_view(['GET'])
def api_request_list(request):
    requests = Request.objects.all()
    serializer = RequestSerializer(requests, many=True)
    return Response(serializer.data)


