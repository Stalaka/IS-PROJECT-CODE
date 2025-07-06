from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView
from procurement.views import (
    CustomLoginView,
    dashboard,
    manufacturer_dashboard,
    request_list,
    purchase_order_list,
    approved_requests,
    new_request,
    new_order,
    account_list,
    api_request_list,
)

urlpatterns = [
    # Admin Panel
    path('admin/', admin.site.urls),

    # Authentication
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    # Dashboards
    path('', dashboard, name='dashboard'),
    path('manufacturer-dashboard/', manufacturer_dashboard, name='manufacturer_dashboard'),

    # Request and Order Views
    path('requests/', request_list, name='request_list'),
    path('purchase-orders/', purchase_order_list, name='purchase_order_list'),
    path('requests/approved/', approved_requests, name='approved_requests'),
    path('requests/new/', new_request, name='new_request'),
    path('orders/new/', new_order, name='new_order'),

    # Account Management
    path('accounts/', account_list, name='account_list'),

    # API Endpoint for Postman test
    path('api/requests/', api_request_list, name='api_request_list'),
]
