from rest_framework import serializers
from .models import Employee, Department, Leadership


class DepartmentSerializer(serializers.ModelSerializer):
    """
    GET /api/departments/?lang=uz  → name = "Moliya bo'limi"
    GET /api/departments/?lang=ru  → name = "Финансовый отдел"
    GET /api/departments/?lang=en  → name = "Finance Department"
    """
    name = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = ['id', 'name', 'name_uz', 'name_ru', 'name_en']

    def get_name(self, obj):
        request = self.context.get('request')
        lang = request.query_params.get('lang', 'uz') if request else 'uz'
        return {
            'uz': obj.name_uz,
            'ru': obj.name_ru,
            'en': obj.name_en,
        }.get(lang, obj.name_uz)


class EmployeeSerializer(serializers.ModelSerializer):
    """
    GET /api/employees/?lang=uz
    GET /api/employees/?lang=ru
    GET /api/employees/?lang=en
    """
    department_name = serializers.SerializerMethodField()
    full_name       = serializers.SerializerMethodField()
    position        = serializers.SerializerMethodField()
    image           = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = [
            'id',
            'department',
            'department_name',
            'full_name',
            'full_name_uz', 'full_name_ru', 'full_name_en',
            'position',
            'position_uz', 'position_ru', 'position_en',
            'floor', 'room', 'phone', 'image',
        ]

    def _lang(self):
        request = self.context.get('request')
        return request.query_params.get('lang', 'uz') if request else 'uz'

    def get_department_name(self, obj):
        if not obj.department:
            return ''
        return {
            'uz': obj.department.name_uz,
            'ru': obj.department.name_ru,
            'en': obj.department.name_en,
        }.get(self._lang(), obj.department.name_uz)

    def get_full_name(self, obj):
        return {
            'uz': obj.full_name_uz,
            'ru': obj.full_name_ru,
            'en': obj.full_name_en,
        }.get(self._lang(), obj.full_name_uz)

    def get_position(self, obj):
        return {
            'uz': obj.position_uz,
            'ru': obj.position_ru,
            'en': obj.position_en,
        }.get(self._lang(), obj.position_uz)

    def get_image(self, obj):
        if not obj.image:
            return None
        image_str = str(obj.image)
        # Agar Supabase URL bo'lsa — to'g'ridan qaytaramiz
        if image_str.startswith('http'):
            return image_str
        # Agar local path bo'lsa — to'liq URL qilamiz
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.image.url)
        return image_str


class LeadershipSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    position  = serializers.SerializerMethodField()
    image     = serializers.SerializerMethodField()

    class Meta:
        model = Leadership
        fields = [
            'id',
            'full_name',
            'full_name_uz', 'full_name_ru', 'full_name_en',
            'position',
            'position_uz', 'position_ru', 'position_en',
            'image', 'order',
        ]

    def _lang(self):
        request = self.context.get('request')
        return request.query_params.get('lang', 'uz') if request else 'uz'

    def get_full_name(self, obj):
        return getattr(obj, f'full_name_{self._lang()}', None) or obj.full_name_uz

    def get_position(self, obj):
        return getattr(obj, f'position_{self._lang()}', None) or obj.position_uz

    def get_image(self, obj):
        if not obj.image:
            return None
        image_str = str(obj.image)
        # Agar Supabase URL bo'lsa — to'g'ridan qaytaramiz
        if image_str.startswith('http'):
            return image_str
        # Agar local path bo'lsa — to'liq URL qilamiz
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.image.url)
        return image_str
