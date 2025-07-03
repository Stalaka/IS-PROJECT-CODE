from django import forms
from .models import Request, PurchaseOrder

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['item_name', 'quantity']

class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ['item_name', 'quantity', 'supplier']
