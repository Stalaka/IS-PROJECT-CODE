from django.shortcuts import render
from rest_framework import viewsets
from .models import ProcurementRequest
from .serializers import ProcurementRequestSerializer

class ProcurementRequestViewSet(viewsets.ModelViewSet):
    queryset = ProcurementRequest.objects.all()
    serializer_class = ProcurementRequestSerializer
