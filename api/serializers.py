from rest_framework import serializers
from .models import Employee, Department, Leadership

class EmployeeSerializer(serializers.ModelSerializer):
    # Bo'lim nomini xavfsiz olish (agar bo'lim o'chib ketgan bo'lsa ham xato bermaydi)
    department_name = serializers.CharField(source='department.name_uz', read_only=True, default="")
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
    class Meta:
        model = Leadership
        fields = '__all__'