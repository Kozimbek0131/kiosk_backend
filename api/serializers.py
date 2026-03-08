class EmployeeSerializer(serializers.ModelSerializer):
    # ID raqami (5, 6) o'rniga bo'lim nomini matn ko'rinishida chiqarish
    department = serializers.ReadOnlyField(source='department.name_uz')
    
    # Telefon raqami bo'sh bo'lishiga ruxsat beramiz
    phone = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        # Barcha maydonlar ro'yxatda borligini tekshiring
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