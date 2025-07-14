from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView

# Import views once as alias
from procurement import views as procurement_views

urlpatterns = [
    # Admin Panel
    path('admin/', admin.site.urls),

    # Authentication
    path('login/', procurement_views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    # Dashboards
    path('', procurement_views.dashboard, name='dashboard'),
    path('manufacturer-dashboard/', procurement_views.manufacturer_dashboard, name='manufacturer_dashboard'),

    # Manufacturer Updates
    path('manufacturer/update/', procurement_views.update_production, name='update_production'),
    path('manufacturer/update/<int:order_id>/', procurement_views.update_production_status, name='update_production_status'),

    # Requests and Orders
    path('requests/', procurement_views.request_list, name='request_list'),
    path('purchase-orders/', procurement_views.purchase_order_list, name='purchase_order_list'),
    path('requests/approved/', procurement_views.approved_requests, name='approved_requests'),
    path('requests/new/', procurement_views.new_request, name='new_request'),
    path('orders/new/', procurement_views.new_order, name='new_order'),

    # Account Management
    path('accounts/', procurement_views.account_list, name='account_list'),

    # API Endpoint
    path('api/requests/', procurement_views.api_request_list, name='api_request_list'),

    # Item Management
    path('items/', procurement_views.item_list, name='item_list'),
    path('items/add/', procurement_views.add_item, name='add_item'),
    path('items/<int:item_id>/update/', procurement_views.update_rate, name='update_rate'),

    # Vendor Management
    path('vendors/', procurement_views.vendor_list, name='vendor_list'),
]
