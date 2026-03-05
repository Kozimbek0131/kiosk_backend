from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Employee, Leadership
from .serializers import EmployeeSerializer, LeadershipSerializer

# --- 1. Xodimlar Ro'yxati (Qidiruv va Filtr bilan) ---
class EmployeeListView(generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    
    # Filtrlash, Qidiruv va Saralash modullarini ulash
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
    
    # SARALASH: Qavat va xona raqami bo'yicha tartiblash
    ordering_fields = ['floor', 'room', 'full_name_uz']
    ordering = ['floor', 'room'] # Standart holatda qavat bo'yicha chiqadi

# --- 2. Rahbariyat Ro'yxati ---
class LeadershipListView(generics.ListAPIView):
    queryset = Leadership.objects.all()
    serializer_class = LeadershipSerializer
    # Rahbarlar modelda ko'rsatilgan 'order' bo'yicha avtomatik saralanadi