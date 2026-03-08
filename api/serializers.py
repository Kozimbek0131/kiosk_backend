from rest_framework import serializers
from .models import Employee, Department, Leadership

class EmployeeSerializer(serializers.ModelSerializer):
    # Bo'lim ID raqami o'rniga nomini ko'rsatish
    department = serializers.ReadOnlyField(source='department.name_uz')
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = [
            'id', 'full_name_uz', 'full_name_ru', 'full_name_en', 
            'position_uz', 'position_ru', 'position_en', 
            'department', 'floor', 'room', 'phone', 'image_url'
        ]

    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None

class LeadershipSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Leadership
        fields = '__all__'

    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None