from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView

# Import views once as alias
from procurement import views as procurement_views

urlpatterns = [
    # Admin Panel
    path('admin/', admin.site.urls),
    path('api/login/', procurement_views.api_login, name='api_login'),
    path('api/procure/', procurement_views.api_procure, name='api_procure'),
    path('api/user/orders/', procurement_views.api_request_list, name='api_request_list'),
    path('api/purchase-orders/', procurement_views.api_purchase_order_list, name='api_purchase_order_list'),
    path('api/orders/<int:order_id>/update/', procurement_views.api_update_status, name='api_update_status'),

   
    
    # Authentication 
    path('login/', procurement_views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    # Dashboards
    path('', procurement_views.dashboard, name='dashboard'),
    path('manufacturer-dashboard/', procurement_views.manufacturer_dashboard, name='manufacturer_dashboard'),

    # Manufacturer Updates
    path('manufacturer/update/', procurement_views.update_production, name='update_production'),
    path('manufacturer/update/<int:order_id>/', procurement_views.update_production_status, name='update_production_status'),

    # Requests and Orders (Web)
    path('requests/', procurement_views.request_list, name='request_list'),
    path('purchase-orders/', procurement_views.purchase_order_list, name='purchase_order_list'),
    path('requests/approved/', procurement_views.approved_requests, name='approved_requests'),
    path('requests/new/', procurement_views.new_request, name='new_request'),
    path('orders/new/', procurement_views.new_order, name='new_order'),

    # Account Management
    path('accounts/', procurement_views.account_list, name='account_list'),

    # Item Management
    path('items/', procurement_views.item_list, name='item_list'),
    path('items/add/', procurement_views.add_item, name='add_item'),
    path('items/<int:item_id>/update/', procurement_views.update_rate, name='update_rate'),
]