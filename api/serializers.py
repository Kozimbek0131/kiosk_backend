from rest_framework import serializers
from .models import Employee, Department

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    # Bo'lim ma'lumotlarini ham to'liq chiqarish uchun:
    department = DepartmentSerializer(read_only=True)
    
    class Meta:
        model = Employee
        fields = '__all__'