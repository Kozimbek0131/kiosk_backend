from django.contrib import admin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from import_export.admin import ImportExportModelAdmin
from .models import Employee, Department, Leadership

class EmployeeResource(resources.ModelResource):
    department = fields.Field(
        column_name='department',
        attribute='department',
        widget=ForeignKeyWidget(Department, 'name_uz')
    )
    class Meta:
        model = Employee
        fields = ('id', 'full_name_uz', 'full_name_ru', 'full_name_en', 
                  'position_uz', 'position_ru', 'position_en', 
                  'department', 'floor', 'room', 'phone')

@admin.register(Employee)
class EmployeeAdmin(ImportExportModelAdmin):
    resource_class = EmployeeResource
    list_display = ('full_name_uz', 'department', 'floor', 'room')
    search_fields = ('full_name_uz', 'phone')
    list_filter = ('department', 'floor')

@admin.register(Leadership)
class LeadershipAdmin(ImportExportModelAdmin):
    list_display = ('full_name_uz', 'position_uz', 'order')
    list_editable = ('order',)
    search_fields = ('full_name_uz', 'position_uz')

@admin.register(Department)
class DepartmentAdmin(ImportExportModelAdmin):
    list_display = ('name_uz', 'name_ru', 'name_en')