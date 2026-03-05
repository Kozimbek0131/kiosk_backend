from django.contrib import admin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from import_export.admin import ImportExportModelAdmin
from .models import Employee, Department

# Bo'limlarni nomiga qarab avtomatik bog'lash uchun resurs
class EmployeeResource(resources.ModelResource):
    department = fields.Field(
        column_name='department',
        attribute='department',
        widget=ForeignKeyWidget(Department, 'name_uz') # Excelda bo'lim nomini yozsangiz ham bo'ladi
    )

    class Meta:
        model = Employee
        # Exceldagi ustunlar tartibi
        fields = ('id', 'full_name_uz', 'full_name_ru', 'full_name_en', 
                  'position_uz', 'position_ru', 'position_en', 
                  'department', 'floor', 'room', 'phone')

@admin.register(Employee)
class EmployeeAdmin(ImportExportModelAdmin):
    resource_class = EmployeeResource
    list_display = ('full_name_uz', 'department', 'floor', 'room')
    search_fields = ('full_name_uz',)
    list_filter = ('department', 'floor')

@admin.register(Department)
class DepartmentAdmin(ImportExportModelAdmin):
    list_display = ('name_uz', 'name_ru', 'name_en')