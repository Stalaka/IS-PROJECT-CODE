from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from .models import Item, RateHistory, Vendor, AuditLog
from .forms import ItemForm, RateUpdateForm

# Helper function to log actions
def log_action(user, action, details=""):
    AuditLog.objects.create(user=user, action=action, details=details)


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


# --- Admin: View Vendor List ---
@login_required
def vendor_list(request):
    vendors = Vendor.objects.all()
    return render(request, 'vendor_list.html', {'vendors': vendors})


