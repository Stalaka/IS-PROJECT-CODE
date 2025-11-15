import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import (
    Item, RateHistory, AuditLog,
    Request, PurchaseOrder, ProductionUpdate
)
from .forms import (
    ItemForm, RateUpdateForm, ProductionUpdateForm,
    RequestForm, PurchaseOrderForm
)

# ==========================================
#           WEB VIEWS (For Browser)
# ==========================================

# --- Custom Login View with Role-Based Redirect ---
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

# --- Helper function to log actions ---
def log_action(user, action, details=""):
    AuditLog.objects.create(user=user, action=action, details=details)

# --- Dashboard for Admin ---
@login_required
def dashboard(request):
    return render(request, 'procurement.html')

# --- Procurement Officer: View List of Items ---
@login_required
def item_list(request):
    items = Item.objects.all()
    return render(request, 'item_list.html', {'items': items})

# --- Procurement Officer: Add New Item ---
@login_required
def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save()
            log_action(request.user, "Added New Item", f"Item: {item.name}, Rate: {item.current_rate}")
            messages.success(request, "New item added.")
            return redirect('item_list')
    else:
        form = ItemForm()
    return render(request, 'add_item.html', {'form': form})

# --- Procurement Officer: Update Item Rate ---
@login_required
def update_rate(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        form = RateUpdateForm(request.POST)
        if form.is_valid():
            old_rate = item.current_rate
            new_rate = form.cleaned_data['new_rate']
            item.current_rate = new_rate
            item.save()

            RateHistory.objects.create(
                item=item,
                old_rate=old_rate,
                new_rate=new_rate,
                changed_by=request.user
            )

            log_action(request.user, "Updated Item Rate", f"{item.name}: {old_rate} -> {new_rate}")
            messages.success(request, f"Rate updated for item '{item.name}'.")
            return redirect('item_list')
    else:
        form = RateUpdateForm(initial={'new_rate': item.current_rate})
    return render(request, 'update_rate.html', {'form': form, 'item': item})


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

# --- Manufacturer: Submit Production Update via Form ---
@login_required
def update_production(request):
    if request.method == 'POST':
        form = ProductionUpdateForm(request.POST)
        if form.is_valid():
            update = form.save(commit=False)
            update.manufacturer = request.user
            update.save()
            messages.success(request, "Production update submitted successfully.")
            return redirect('manufacturer_dashboard')
    else:
        form = ProductionUpdateForm()
    return render(request, 'update_production.html', {'form': form})

# --- Manufacturer: Quick Update Production Status ---
@login_required
def update_production_status(request, order_id):
    order = get_object_or_404(PurchaseOrder, id=order_id)
    update, created = ProductionUpdate.objects.get_or_create(
        order=order,
        manufacturer=request.user
    )
    if request.method == 'POST':
        status = request.POST.get('completion_status')
        deadline = request.POST.get('production_deadline')
        if status:
            update.completion_status = status
        if deadline:
            update.production_deadline = deadline
        update.save()
        messages.success(request, f"Production status updated for Order #{order.id}")
        return redirect('manufacturer_dashboard')
    return render(request, 'update_status.html', {'order': order, 'update': update})

# --- Procurement Officer: View All Requests ---
@login_required
def request_list(request):
    requests = Request.objects.all()
    return render(request, 'requests.html', {'requests': requests})

# --- Procurement Officer: View Approved Requests ---
@login_required
def approved_requests(request):
    approved = Request.objects.filter(status='approved')
    return render(request, 'approved_requests.html', {'requests': approved})

# --- Procurement Officer: Create New Request ---
@login_required
def new_request(request):
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            new_req = form.save(commit=False)
            new_req.requester = request.user
            new_req.save()
            messages.success(request, "Material request submitted.")
            return redirect('request_list')
    else:
        form = RequestForm()
    return render(request, 'new_request.html', {'form': form})

# --- Supplier: View All Purchase Orders ---
@login_required
def purchase_order_list(request):
    orders = PurchaseOrder.objects.all()
    return render(request, 'purchase_orders.html', {'orders': orders})

# --- Procurement Officer: Create New Purchase Order ---
@login_required
def new_order(request):
    if request.method == 'POST':
        form = PurchaseOrderForm(request.POST, request.FILES)
        if form.is_valid():
            order = form.save()
            log_action(request.user, "Created New Purchase Order", f"Order: {order.item_name}, Quantity: {order.quantity}")
            messages.success(request, "Purchase order created successfully.")
            return redirect('purchase_order_list')
    else:
        form = PurchaseOrderForm()
    return render(request, 'new_order.html', {'form': form})

# --- Admin: View All User Accounts ---
@login_required
def account_list(request):
    if not request.user.is_superuser and not request.user.groups.filter(name='Admin').exists():
        messages.error(request, "Access denied. Admins only.")
        return redirect('dashboard')

    users = User.objects.all().order_by('username')
    return render(request, 'account.html', {'users': users})


# ==========================================
#       MOBILE APP API ENDPOINTS
# ==========================================

# --- API: Mobile Login ---
@csrf_exempt
def api_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            
            user = authenticate(username=username, password=password)
            
            if user is not None:
                return JsonResponse({
                    'token': 'mobile-app-access-token-12345',
                    'user_id': user.id,
                    'message': 'Login Successful'
                })
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
            
    return JsonResponse({'error': 'POST request required'}, status=405)

# --- API: Return Material Requests as JSON ---
def api_request_list(request):
    # Note: Removed @login_required so mobile app can access it with dummy token
    requests = Request.objects.all()
    
    # Map DB fields to Android Expected Fields
    data = []
    for r in requests:
        data.append({
            'material_id': r.id,
            'material_name': r.item_name,      # Android expects 'material_name'
            'current_stock': r.quantity,       # Android expects 'current_stock'
            'procurement_status': r.status     # Android expects 'procurement_status'
        })
        
    return JsonResponse(data, safe=False)

# --- API: Return Purchase Orders as JSON ---
def api_purchase_order_list(request):
    orders = PurchaseOrder.objects.all()
    
    data = []
    for order in orders:
        data.append({
            'order_id': order.id,
            'item_name': order.item_name,  
            'quantity': order.quantity,
            'status': getattr(order, 'status', 'Ordered'), 
            'supplier': str(order.supplier) if hasattr(order, 'supplier') else 'Unknown'
        })
        
    return JsonResponse(data, safe=False)

# --- API: Submit Procurement Request ---
@csrf_exempt
def api_procure(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Map Android keys to DB keys
            item_name = data.get('material_name') 
            quantity = data.get('current_stock')  
            status = data.get('procurement_status')
            
            if not item_name or not quantity:
                return JsonResponse({'error': 'Missing name or quantity'}, status=400)

            # Assign to the first available user (fallback for dummy token)
            requester_user = User.objects.filter(is_superuser=True).first() or User.objects.first()

            new_req = Request.objects.create(
                item_name=item_name,
                quantity=quantity,
                status=status or 'Pending',
                requester=requester_user
            )
            
            return JsonResponse({'message': 'Request created successfully', 'id': new_req.id})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'POST request required'}, status=405)

# --- API: Update Order Status ---
@csrf_exempt
def api_update_status(request, order_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            new_status = data.get('status')
            
            # Find the request by ID
            order = Request.objects.get(id=order_id)
            order.status = new_status
            order.save()
            
            return JsonResponse({'message': 'Status updated successfully'})
        except Request.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'POST request required'}, status=405)