from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Employee
from .serializers import EmployeeSerializer

class EmployeeListView(generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    
    # Filtrlash modullarini ulash
    filter_backends = [
        DjangoFilterBackend, 
        filters.SearchFilter, 
        filters.OrderingFilter
    ]
    
    # QIDIRUV: Ism, lavozim va telefon raqami bo'yicha
    search_fields = [
        'full_name_uz', 'full_name_ru', 'full_name_en', 
        'position_uz', 'phone' 
    ]
    
    # FILTR: Qavat va bo'lim bo'yicha
    filterset_fields = ['floor', 'department']
    
    # SARALASH: Qavat va xona bo'yicha
    ordering_fields = ['floor', 'room']
    ordering = ['floor', 'room']