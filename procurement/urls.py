from django.urls import path, include
from rest_framework import routers
from .views import ProcurementRequestViewSet

router = routers.DefaultRouter()
router.register(r'procurement-requests', ProcurementRequestViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
