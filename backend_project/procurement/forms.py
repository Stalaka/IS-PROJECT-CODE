from django import forms
from .models import Request, PurchaseOrder, ProductionUpdate

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
        widgets = {
            'item_name': forms.TextInput(attrs={'placeholder': 'Enter item name'}),
        }

class ProductionUpdateForm(forms.ModelForm):
    class Meta:
        model = ProductionUpdate
        fields = [
            'order',
            'start_date',
            'end_date',
            'production_deadline',
            'completion_status',
            'is_completed',
            'notes',
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'production_deadline': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
