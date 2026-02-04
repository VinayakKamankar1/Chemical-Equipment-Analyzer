from rest_framework import serializers
from .models import DatasetSummary
from django.contrib.auth.models import User


class DatasetSummarySerializer(serializers.ModelSerializer):
    equipment_type_distribution = serializers.SerializerMethodField()
    
    class Meta:
        model = DatasetSummary
        fields = [
            'id', 'filename', 'uploaded_at', 'total_equipment_count',
            'avg_flowrate', 'avg_pressure', 'avg_temperature',
            'equipment_type_distribution'
        ]
        read_only_fields = ['id', 'uploaded_at']
    
    def get_equipment_type_distribution(self, obj):
        return obj.get_type_distribution()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        read_only_fields = ['id']

