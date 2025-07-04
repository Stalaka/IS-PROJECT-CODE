from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from procurement.views import CustomLoginView  
from procurement import views as procurement_views

urlpatterns = [
    # Admin Panel
    path('admin/', admin.site.urls),

    # Authentication 
    path('login/', CustomLoginView.as_view(), name='login'),
    # Dashboard (Home)
    path('', procurement_views.dashboard, name='dashboard'),

    # Other Views
    path('requests/', procurement_views.request_list, name='request_list'),
    path('purchase-orders/', procurement_views.purchase_order_list, name='purchase_order_list'),
    path('accounts/', procurement_views.account_list, name='account_list'),
    path('settings/', procurement_views.settings_page, name='settings'),

    # Form Views
    path('requests/new/', procurement_views.new_request, name='new_request'),
    path('orders/new/', procurement_views.new_order, name='new_order'),
    path('requests/approved/', procurement_views.approved_requests, name='approved_requests'),
]

from django.contrib.auth.views import LogoutView

path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

