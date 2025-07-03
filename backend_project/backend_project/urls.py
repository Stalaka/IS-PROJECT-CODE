from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from procurement import views as procurement_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Dashboard
    path('', procurement_views.dashboard, name='dashboard'),

    # Additional views
    path('requests/', procurement_views.request_list, name='request_list'),
    path('purchase-orders/', procurement_views.purchase_order_list, name='purchase_order_list'),
    path('accounts/', procurement_views.account_list, name='account_list'),
    path('settings/', procurement_views.settings_page, name='settings'),

    # Forms
    path('requests/new/', procurement_views.new_request, name='new_request'),
    path('orders/new/', procurement_views.new_order, name='new_order'),
    path('requests/approved/', procurement_views.approved_requests, name='approved_requests'),
]
