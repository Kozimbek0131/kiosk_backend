class EmployeeSerializer(serializers.ModelSerializer):
    # 1. Bo'lim nomini ID raqami emas, matn ko'rinishida chiqaradi
    department = serializers.ReadOnlyField(source='department.name_uz')
    
    # 2. Rasmning to'liq manzili (URL) hosil bo'lishini ta'minlaydi
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        # 3. 'phone' maydoni JSON'da chiqishi uchun uni aniq ko'rsatib qo'yamiz
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