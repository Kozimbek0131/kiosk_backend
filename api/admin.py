from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Employee, Department

@admin.register(Employee)
class EmployeeAdmin(ImportExportModelAdmin):
    # Ro'yxatda ko'rinadigan ustunlar
    list_display = ('full_name_uz', 'department', 'floor', 'room', 'phone')
    # Qidiruv maydonlari
    search_fields = ('full_name_uz', 'full_name_ru', 'full_name_en')
    # Filtrlash imkoniyati
    list_filter = ('department', 'floor')

@admin.register(Department)
class DepartmentAdmin(ImportExportModelAdmin):
    list_display = ('name_uz', 'name_ru', 'name_en')