from django.contrib import admin
from .models import Department, Employee

admin.site.site_header = "Akademiya Kiosk Admin"
admin.site.index_title = "Ma'lumotlarni boshqarish"

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name_uz', 'name_ru', 'name_en')
    search_fields = ('name_uz',)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('full_name_uz', 'department', 'floor', 'room', 'phone')
    list_filter = ('department', 'floor')
    search_fields = ('full_name_uz', 'full_name_ru', 'full_name_en', 'position_uz')
    list_editable = ('floor', 'room', 'phone') # Admin panelning o'zida tahrirlash uchun