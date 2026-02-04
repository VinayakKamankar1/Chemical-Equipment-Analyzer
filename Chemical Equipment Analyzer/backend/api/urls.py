from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('upload/', views.upload_csv, name='upload_csv'),
    path('history/', views.get_history, name='get_history'),
    path('summary/<int:summary_id>/', views.get_summary, name='get_summary'),
    path('summary/<int:summary_id>/pdf/', views.generate_pdf, name='generate_pdf'),
]

