from rest_framework import serializers
from .models import Employee, Department, Leadership

class BaseLanguageSerializer(serializers.ModelSerializer):
    def get_lang(self):
        request = self.context.get('request')
        if request:
            return request.query_params.get('lang') or request.headers.get('Accept-Language', 'uz')[:2]
        return 'uz'

    def translate(self, obj, field_prefix):
        lang = self.get_lang()
        val = getattr(obj, f'{field_prefix}_{lang}', None)
        if not val:
            val = getattr(obj, f'{field_prefix}_uz', "")
        return val

class DepartmentSerializer(BaseLanguageSerializer):
    name = serializers.SerializerMethodField()
    class Meta:
        model = Department
        fields = ['id', 'name', 'name_uz', 'name_ru', 'name_en']
    def get_name(self, obj):
        return self.translate(obj, 'name')

class EmployeeSerializer(BaseLanguageSerializer):
    department_name = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    position = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = [
            'id', 'department', 'department_name', 'full_name', 
            'full_name_uz', 'full_name_ru', 'full_name_en',
            'position', 'position_uz', 'position_ru', 'position_en',
            'floor', 'room', 'phone', 'image', 'image_url'
        ]

    def get_department_name(self, obj):
        if obj.department:
            return self.translate(obj.department, 'name')
        return ""

    def get_full_name(self, obj):
        return self.translate(obj, 'full_name')

    def get_position(self, obj):
        return self.translate(obj, 'position')

    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None

class LeadershipSerializer(BaseLanguageSerializer):
    full_name = serializers.SerializerMethodField()
    position = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Leadership
        fields = [
            'id', 'full_name', 'full_name_uz', 'full_name_ru', 'full_name_en',
            'position', 'position_uz', 'position_ru', 'position_en',
            'image', 'image_url', 'order'
        ]

    def get_full_name(self, obj):
        return self.translate(obj, 'full_name')

    def get_position(self, obj):
        return self.translate(obj, 'position')

    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None