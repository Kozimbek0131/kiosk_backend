import time
from django.contrib import admin
from django.utils.html import format_html
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.contrib import messages
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from import_export.admin import ImportExportModelAdmin
from .models import Employee, Department, Leadership

# --- Resource qismi (Excel import/export uchun) ---
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
                  'department', 'floor', 'room', 'phone', 'order')

# --- Employee Admin ---
@admin.register(Employee)
class EmployeeAdmin(ImportExportModelAdmin):
    resource_class = EmployeeResource
    list_display = ('order', 'photo_preview', 'full_name_uz', 'get_dept', 'floor', 'room', 'phone', 'upload_button')
    list_editable = ('order',)
    list_display_links = ('full_name_uz',) 
    list_filter = ('department', 'floor')
    search_fields = ('full_name_uz', 'phone', 'position_uz')
    readonly_fields = ('photo_preview',)
    ordering = ('department__order', 'order')

    def get_dept(self, obj):
        return obj.department.name_uz if obj.department else "—"
    get_dept.short_description = 'Bo‘lim'

    def photo_preview(self, obj):
        if obj.image:
            try:
                return format_html('<img src="{}" width="50" height="50" style="object-fit:cover;border-radius:8px;border:1px solid #ddd"/>', obj.image.url)
            except:
                return "Rasmda xato"
        # Argument qo'shildi
        return format_html('<span style="color:#999">{}</span>', "Rasm yo‘q")
    photo_preview.short_description = 'Rasm'

    def upload_button(self, obj):
        return format_html(
            '<form method="post" enctype="multipart/form-data" action="upload-photo/{}/">'
            '<input type="file" name="photo" accept="image/*" style="font-size:10px;width:125px" onchange="this.form.submit()">'
            '</form>',
            obj.id
        )
    upload_button.short_description = 'Rasm yuklash'

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path('upload-photo/<int:employee_id>/', self.admin_site.admin_view(csrf_exempt(self.upload_photo_view)))
        ]
        return custom + urls

    def upload_photo_view(self, request, employee_id):
        if request.method == 'POST' and request.FILES.get('photo'):
            try:
                emp = Employee.objects.get(id=employee_id)
                emp.image = request.FILES['photo']
                emp.save()
                messages.success(request, f"{emp.full_name_uz} rasmi muvaffaqiyatli yangilandi!")
            except Exception as e:
                messages.error(request, f"Xatolik: {str(e)}")
        return redirect('..')

# --- Leadership Admin ---
@admin.register(Leadership)
class LeadershipAdmin(ImportExportModelAdmin):
    list_display = ('order', 'photo_preview', 'full_name_uz', 'rank_uz', 'phone', 'upload_button')
    list_editable = ('order', 'rank_uz')
    list_display_links = ('full_name_uz',)
    readonly_fields = ('photo_preview',)
    ordering = ('order',)
    
    fieldsets = (
        ("Asosiy", {'fields': ('full_name_uz', 'full_name_ru', 'full_name_en', 'order')}),
        ("Unvon va Lavozim", {'fields': ('rank_uz', 'rank_ru', 'rank_en', 'position_uz', 'position_ru', 'position_en')}),
         ("Aloqa", {'fields': ('phone', 'email', 'work_hours_uz', 'work_hours_ru', 'work_hours_en', 'image')}), # work_hours_en qo'shildi
    )

    def photo_preview(self, obj):
        if obj.image:
            try:
                # {} o'rniga aniq argument uzatish
                return format_html('<img src="{}" width="55" height="55" style="object-fit:cover;border-radius:50%;border:2px solid #fbbf24;padding:2px"/>', obj.image.url)
            except:
                return "Rasmda xato"
        # XATO TUZATILDI: {} va "Rasm yo'q" matni alohida argument qilib berildi
        return format_html('<div style="width:50px;height:50px;border-radius:50%;background:#eee;display:flex;align-items:center;justify-content:center;color:#ccc;font-size:10px;">{}</div>', "Rasm yo‘q")
    photo_preview.short_description = 'Rasm'

    def upload_button(self, obj):
        return format_html(
            '<form method="post" enctype="multipart/form-data" action="upload-leader-photo/{}/">'
            '<input type="file" name="photo" accept="image/*" style="font-size:10px;width:125px" onchange="this.form.submit()">'
            '</form>',
            obj.id
        )
    upload_button.short_description = 'Rasm yuklash'

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path('upload-leader-photo/<int:leader_id>/', self.admin_site.admin_view(csrf_exempt(self.upload_leader_photo_view)))
        ]
        return custom + urls

    def upload_leader_photo_view(self, request, leader_id):
        if request.method == 'POST' and request.FILES.get('photo'):
            try:
                leader = Leadership.objects.get(id=leader_id)
                leader.image = request.FILES['photo']
                leader.save()
                messages.success(request, f"{leader.full_name_uz} rasmi yuklandi!")
            except Exception as e:
                messages.error(request, f"Xato: {e}")
        return redirect('..')

# --- Department Admin ---
@admin.register(Department)
class DepartmentAdmin(ImportExportModelAdmin):
    list_display = ('order', 'name_uz', 'name_ru', 'name_en')
    list_editable = ('order',)
    list_display_links = ('name_uz',)
    ordering = ('order',)