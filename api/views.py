from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Employee, Department, Leadership
from .serializers import EmployeeSerializer, DepartmentSerializer, LeadershipSerializer


# ─────────────────────────────────────────────────────────
# 1. BO'LIMLAR RO'YXATI
# GET /api/departments/
# GET /api/departments/?lang=ru
# ─────────────────────────────────────────────────────────
class DepartmentListView(generics.ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


# ─────────────────────────────────────────────────────────
# 2. XODIMLAR RO'YXATI (qidiruv + filtr + til)
# GET /api/employees/
# GET /api/employees/?lang=ru
# GET /api/employees/?search=Karimov
# GET /api/employees/?floor=2&department=3
# ─────────────────────────────────────────────────────────
class EmployeeListView(generics.ListAPIView):
    queryset = Employee.objects.select_related('department').all()
    serializer_class = EmployeeSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    search_fields = [
        'full_name_uz', 'full_name_ru', 'full_name_en',
        'position_uz', 'phone',
    ]

    filterset_fields = ['floor', 'department']

    ordering_fields = ['floor', 'room', 'full_name_uz']
    ordering = ['floor', 'room']

    def get_serializer_context(self):
        # Tilni serializer'ga uzatish uchun MUHIM
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


# ─────────────────────────────────────────────────────────
# 3. RAHBARIYAT RO'YXATI
# GET /api/leadership/
# GET /api/leadership/?lang=en
# ─────────────────────────────────────────────────────────
class LeadershipListView(generics.ListAPIView):
    queryset = Leadership.objects.all()
    serializer_class = LeadershipSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context