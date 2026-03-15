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
            'floor', 'room', 'phone', 'image', 'image_url',
            'order'  # <--- MANA SHU YERGA 'order' QO'SHILDI
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