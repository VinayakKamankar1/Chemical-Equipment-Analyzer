from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone
import pandas as pd
import json
import os
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import inch

from .models import DatasetSummary
from .serializers import DatasetSummarySerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Register a new user"""
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email', '')
    
    if not username or not password:
        return Response(
            {'error': 'Username and password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if User.objects.filter(username=username).exists():
        return Response(
            {'error': 'Username already exists'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = User.objects.create_user(username=username, password=password, email=email)
    token, created = Token.objects.get_or_create(user=user)
    
    return Response({
        'token': token.key,
        'user_id': user.id,
        'username': user.username
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """Login and get authentication token"""
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'error': 'Username and password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = authenticate(username=username, password=password)
    
    if not user:
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    token, created = Token.objects.get_or_create(user=user)
    
    return Response({
        'token': token.key,
        'user_id': user.id,
        'username': user.username
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_csv(request):
    """Upload and parse CSV file, compute analytics, and store summary"""
    if 'file' not in request.FILES:
        return Response(
            {'error': 'No file provided'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    file = request.FILES['file']
    
    # Validate file extension
    if not file.name.endswith('.csv'):
        return Response(
            {'error': 'File must be a CSV file'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Read CSV with pandas
        df = pd.read_csv(file)
        
        # Required columns
        required_columns = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
        
        # Check if all required columns exist (case-insensitive)
        df_columns_lower = [col.strip().lower() for col in df.columns]
        required_lower = [col.lower() for col in required_columns]
        
        missing_columns = []
        column_mapping = {}
        
        for req_col in required_columns:
            req_lower = req_col.lower()
            found = False
            for idx, col in enumerate(df.columns):
                if col.strip().lower() == req_lower:
                    column_mapping[req_col] = col
                    found = True
                    break
            if not found:
                missing_columns.append(req_col)
        
        if missing_columns:
            return Response(
                {'error': f'Missing required columns: {", ".join(missing_columns)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Map columns to standard names
        df_standard = df.rename(columns=column_mapping)
        
        # Convert numeric columns, handling errors
        numeric_columns = ['Flowrate', 'Pressure', 'Temperature']
        for col in numeric_columns:
            df_standard[col] = pd.to_numeric(df_standard[col], errors='coerce')
        
        # Remove rows with missing numeric values
        df_standard = df_standard.dropna(subset=numeric_columns)
        
        if len(df_standard) == 0:
            return Response(
                {'error': 'No valid data rows found after processing'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Compute summary statistics
        total_count = len(df_standard)
        avg_flowrate = float(df_standard['Flowrate'].mean())
        avg_pressure = float(df_standard['Pressure'].mean())
        avg_temperature = float(df_standard['Temperature'].mean())
        
        # Equipment type distribution
        type_distribution = df_standard['Type'].value_counts().to_dict()
        # Convert numpy types to native Python types
        type_distribution = {str(k): int(v) for k, v in type_distribution.items()}
        
        # Store summary (keep only last 5 per user)
        summaries = DatasetSummary.objects.filter(user=request.user).order_by('-uploaded_at')
        if summaries.count() >= 5:
            # Delete oldest
            summaries[4:].delete()
        
        # Create new summary
        summary = DatasetSummary.objects.create(
            user=request.user,
            filename=file.name,
            total_equipment_count=total_count,
            avg_flowrate=avg_flowrate,
            avg_pressure=avg_pressure,
            avg_temperature=avg_temperature,
        )
        summary.set_type_distribution(type_distribution)
        summary.save()
        
        # Prepare response data
        response_data = {
            'id': summary.id,
            'filename': summary.filename,
            'uploaded_at': summary.uploaded_at,
            'total_equipment_count': total_count,
            'avg_flowrate': round(avg_flowrate, 2),
            'avg_pressure': round(avg_pressure, 2),
            'avg_temperature': round(avg_temperature, 2),
            'equipment_type_distribution': type_distribution,
            'raw_data': df_standard.to_dict('records')[:100]  # Limit to first 100 rows for response
        }
        
        return Response(response_data, status=status.HTTP_201_CREATED)
        
    except pd.errors.EmptyDataError:
        return Response(
            {'error': 'CSV file is empty'},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {'error': f'Error processing CSV: {str(e)}'},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_history(request):
    """Get upload history (last 5 datasets)"""
    summaries = DatasetSummary.objects.filter(user=request.user).order_by('-uploaded_at')[:5]
    serializer = DatasetSummarySerializer(summaries, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_summary(request, summary_id):
    """Get detailed summary of a specific dataset"""
    try:
        summary = DatasetSummary.objects.get(id=summary_id, user=request.user)
        serializer = DatasetSummarySerializer(summary)
        return Response(serializer.data)
    except DatasetSummary.DoesNotExist:
        return Response(
            {'error': 'Summary not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generate_pdf(request, summary_id):
    """Generate and return PDF report for a dataset summary"""
    try:
        summary = DatasetSummary.objects.get(id=summary_id, user=request.user)
    except DatasetSummary.DoesNotExist:
        return Response(
            {'error': 'Summary not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Create PDF in memory
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    story = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=30,
    )
    
    # Title
    story.append(Paragraph("Chemical Equipment Analysis Report", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # File info
    story.append(Paragraph(f"<b>File:</b> {summary.filename}", styles['Normal']))
    story.append(Paragraph(f"<b>Uploaded:</b> {summary.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Summary Statistics
    story.append(Paragraph("<b>Summary Statistics</b>", styles['Heading2']))
    story.append(Spacer(1, 0.1*inch))
    
    summary_data = [
        ['Metric', 'Value'],
        ['Total Equipment Count', str(summary.total_equipment_count)],
        ['Average Flowrate', f"{summary.avg_flowrate:.2f}"],
        ['Average Pressure', f"{summary.avg_pressure:.2f}"],
        ['Average Temperature', f"{summary.avg_temperature:.2f}"],
    ]
    
    summary_table = Table(summary_data)
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    story.append(summary_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Equipment Type Distribution
    story.append(Paragraph("<b>Equipment Type Distribution</b>", styles['Heading2']))
    story.append(Spacer(1, 0.1*inch))
    
    type_dist = summary.get_type_distribution()
    if type_dist:
        dist_data = [['Equipment Type', 'Count']]
        for eq_type, count in type_dist.items():
            dist_data.append([str(eq_type), str(count)])
        
        dist_table = Table(dist_data)
        dist_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        story.append(dist_table)
    
    # Build PDF
    doc.build(story)
    
    # Get PDF content
    buffer.seek(0)
    pdf_content = buffer.getvalue()
    buffer.close()
    
    # Return PDF as response
    from django.http import HttpResponse
    response = HttpResponse(pdf_content, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="report_{summary.id}.pdf"'
    return response

