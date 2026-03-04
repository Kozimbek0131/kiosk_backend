from rest_framework import generics
from .models import Employee
from .serializers import EmployeeSerializer # Endi bu fayl mavjud

class EmployeeListView(generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer