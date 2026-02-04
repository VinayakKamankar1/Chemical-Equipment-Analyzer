from django.contrib import admin
from .models import DatasetSummary


@admin.register(DatasetSummary)
class DatasetSummaryAdmin(admin.ModelAdmin):
    list_display = ['filename', 'user', 'uploaded_at', 'total_equipment_count']
    list_filter = ['uploaded_at']
    search_fields = ['filename', 'user__username']

