from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Employee, Department, Leadership
from .serializers import EmployeeSerializer, DepartmentSerializer, LeadershipSerializer
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests # Supabase API uchun kerak bo'lishi mumkin

class DepartmentListView(generics.ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class EmployeeListView(generics.ListAPIView):
    queryset = Employee.objects.select_related('department').all()
    serializer_class = EmployeeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['full_name_uz', 'full_name_ru', 'full_name_en', 'position_uz', 'phone']
    filterset_fields = ['floor', 'department']
    ordering = ['floor', 'room']

class LeadershipListView(generics.ListAPIView):
    queryset = Leadership.objects.all().order_by('order')
    serializer_class = LeadershipSerializer

@csrf_exempt
def upload_employee_photo(request, employee_id):
    """Admin panel orqali rasm tanlanganda muammosiz yuklanishi uchun"""
    if request.method == 'POST':
        try:
            employee = Employee.objects.get(id=employee_id)
            photo = request.FILES.get('photo')
            if photo:
                employee.image = photo
                employee.save()
                return JsonResponse({"status": "success", "url": employee.image.url})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)