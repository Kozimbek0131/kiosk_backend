class EmployeeSerializer(serializers.ModelSerializer):
    # Departmentni dinamik qilish uchun MethodField ishlatamiz
    department = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = '__all__'

    def get_department(self, obj):
        # Frontenddan kelayotgan tilni aniqlaymiz (Accept-Language header orqali)
        request = self.context.get('request')
        lang = 'uz' # Standart til
        
        if request and 'Accept-Language' in request.headers:
            # Masalan: 'ru', 'en' yoki 'uz'
            lang = request.headers['Accept-Language'][:2] 
        
        # Tilga qarab tegishli maydonni qaytaramiz
        if lang == 'ru':
            return obj.department.name_ru
        elif lang == 'en':
            return obj.department.name_en
        else:
            return obj.department.name_uz

    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None