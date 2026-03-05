from rest_framework import serializers
from .models import Employee, Department, Leadership

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    # Bo'lim nomini matn ko'rinishida chiqarish
    department_name = serializers.ReadOnlyField(source='department.name_uz')
    # To'liq rasm URL manzili
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = '__all__'

    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None

class LeadershipSerializer(serializers.ModelSerializer):
    # Rahbarlar uchun ham to'liq rasm URL
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Leadership
        fields = '__all__'

    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None