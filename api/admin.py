from django.contrib import admin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from import_export.admin import ImportExportModelAdmin
from .models import Employee, Department, Leadership

# --- 1. Xodimlar (Employee) uchun Import/Export resursi ---
class EmployeeResource(resources.ModelResource):
    # Bo'limni ID raqami bilan emas, nomi (name_uz) bilan Exceldan topish
    department = fields.Field(
        column_name='department',
        attribute='department',
        widget=ForeignKeyWidget(Department, 'name_uz')
    )

    class Meta:
        model = Employee
        # Excel ustunlari tartibi
        fields = ('id', 'full_name_uz', 'full_name_ru', 'full_name_en', 
                  'position_uz', 'position_ru', 'position_en', 
                  'department', 'floor', 'room', 'phone')

@admin.register(Employee)
class EmployeeAdmin(ImportExportModelAdmin):
    resource_class = EmployeeResource
    list_display = ('full_name_uz', 'department', 'floor', 'room')
    # Qidiruvga telefon raqami qo'shildi
    search_fields = ('full_name_uz', 'phone') 
    list_filter = ('department', 'floor')

# --- 2. Rahbariyat (Leadership) uchun Import/Export resursi ---
class LeadershipResource(resources.ModelResource):
    class Meta:
        model = Leadership
        fields = ('id', 'full_name_uz', 'full_name_ru', 'full_name_en', 
                  'position_uz', 'position_ru', 'position_en', 'order')

@admin.register(Leadership)
class LeadershipAdmin(ImportExportModelAdmin):
    resource_class = LeadershipResource
    list_display = ('full_name_uz', 'position_uz', 'order')
    # Tartib raqamini ro'yxatning o'zida tahrirlash imkoniyati
    list_editable = ('order',) 
    search_fields = ('full_name_uz', 'position_uz')

# --- 3. Bo'limlar (Department) uchun Import/Export resursi ---
@admin.register(Department)
class DepartmentAdmin(ImportExportModelAdmin):
    list_display = ('name_uz', 'name_ru', 'name_en')
    search_fields = ('name_uz',)