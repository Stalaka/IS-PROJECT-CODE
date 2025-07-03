from rest_framework import serializers
from .models import ProcurementRequest

class ProcurementRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcurementRequest
        fields = '__all__'
