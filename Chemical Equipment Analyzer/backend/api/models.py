from django.db import models
from django.contrib.auth.models import User
import json


class DatasetSummary(models.Model):
    """Store summary of uploaded CSV datasets"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    # Summary statistics
    total_equipment_count = models.IntegerField()
    avg_flowrate = models.FloatField()
    avg_pressure = models.FloatField()
    avg_temperature = models.FloatField()
    
    # Equipment type distribution stored as JSON
    equipment_type_distribution = models.TextField()  # JSON string
    
    # Raw data summary (optional, for quick reference)
    raw_data_summary = models.TextField(null=True, blank=True)  # JSON string
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def get_type_distribution(self):
        """Parse and return equipment type distribution as dict"""
        try:
            return json.loads(self.equipment_type_distribution)
        except:
            return {}
    
    def set_type_distribution(self, distribution):
        """Store equipment type distribution as JSON string"""
        self.equipment_type_distribution = json.dumps(distribution)
    
    def __str__(self):
        return f"{self.filename} - {self.uploaded_at}"

