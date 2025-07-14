from django import forms
from .models import Request, PurchaseOrder, ProductionUpdate, Item


class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['item_name', 'quantity']
        widgets = {
            'item_name': forms.TextInput(attrs={'placeholder': 'Enter item name'}),
        }


class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ['item_name', 'quantity', 'supplier', 'purchase_document']


class ProductionUpdateForm(forms.ModelForm):
    class Meta:
        model = ProductionUpdate
        fields = [
            'order', 'start_date', 'end_date',
            'production_deadline', 'completion_status',
            'is_completed', 'notes'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'production_deadline': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


# ✅ This fixes the missing import error
class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'current_rate']


# ✅ Also define this as it's being imported in your views
class RateUpdateForm(forms.Form):
    new_rate = forms.DecimalField(max_digits=10, decimal_places=2)
