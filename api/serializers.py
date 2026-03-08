class EmployeeSerializer(serializers.ModelSerializer):
    # Har bir til uchun alohida maydon yaratamiz
    department_uz = serializers.ReadOnlyField(source='department.name_uz')
    department_ru = serializers.ReadOnlyField(source='department.name_ru')
    department_en = serializers.ReadOnlyField(source='department.name_en')
    
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        # fields ichiga yangi yaratgan maydonlarimizni qo'shamiz
        fields = [
            'id', 'full_name_uz', 'full_name_ru', 'full_name_en', 
            'position_uz', 'position_ru', 'position_en', 
            'department_uz', 'department_ru', 'department_en', 
            'floor', 'room', 'phone', 'image_url'
        ]

    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None