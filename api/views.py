from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Employee, Department, Leadership
from .serializers import EmployeeSerializer, DepartmentSerializer, LeadershipSerializer

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

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class LeadershipListView(generics.ListAPIView):
    queryset = Leadership.objects.all().order_by('order')
    serializer_class = LeadershipSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context