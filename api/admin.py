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

# Employee uchun resurs
class EmployeeResource(resources.ModelResource):
    department = fields.Field(
        column_name='department',
        attribute='department',
        widget=ForeignKeyWidget(Department, 'name_uz')
    )
    class Meta:
        model = Employee
        fields = ('id', 'full_name_uz', 'department', 'floor', 'room', 'phone')

@admin.register(Employee)
class EmployeeAdmin(ImportExportModelAdmin):
    resource_class = EmployeeResource
    list_display = ('id', 'full_name_uz', 'floor', 'room', 'photo_preview', 'upload_button')
    list_filter = ('department', 'floor')
    search_fields = ('full_name_uz', 'phone')
    readonly_fields = ('photo_preview',)

    def photo_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="60" height="75" style="object-fit:cover;border-radius:4px"/>', obj.image.url)
        return "—"

    def upload_button(self, obj):
        return format_html(
            '<form method="post" enctype="multipart/form-data" action="/admin/api/employee/upload-photo/{}/">'
            '<input type="file" name="photo" accept="image/*" style="font-size:10px;width:130px" onchange="this.form.submit()">'
            '</form>',
            obj.id
        )

    def get_urls(self):
        urls = super().get_urls()
        custom = [path('upload-photo/<int:employee_id>/', csrf_exempt(self.admin_site.admin_view(self.upload_photo_view)))]
        return custom + urls

    def upload_photo_view(self, request, employee_id):
        if request.method == 'POST' and request.FILES.get('photo'):
            try:
                emp = Employee.objects.get(id=employee_id)
                emp.image = request.FILES['photo']
                emp.save()
                messages.success(request, f"{emp.full_name_uz} rasmi yuklandi!")
            except Exception as e:
                messages.error(request, f"Xato: {e}")
        return redirect('/admin/api/employee/')

@admin.register(Leadership)
class LeadershipAdmin(ImportExportModelAdmin):
    # FAQAT 100% BOR MAYDONLARNI QOLDIRDIK:
    list_display = ('full_name_uz', 'order', 'photo_preview', 'upload_button')
    list_editable = ('order',)
    search_fields = ('full_name_uz',)
    readonly_fields = ('photo_preview',)

    def photo_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="60" height="75" style="object-fit:cover;border-radius:4px"/>', obj.image.url)
        return '—'

    def upload_button(self, obj):
        return format_html(
            '<form method="post" enctype="multipart/form-data" action="/admin/api/leadership/upload-leader-photo/{}/">'
            '<input type="file" name="photo" accept="image/*" style="font-size:10px;width:130px" onchange="this.form.submit()">'
            '</form>',
            obj.id
        )

    def get_urls(self):
        urls = super().get_urls()
        custom = [path('upload-leader-photo/<int:leader_id>/', csrf_exempt(self.admin_site.admin_view(self.upload_leader_photo_view)))]
        return custom + urls

    def upload_leader_photo_view(self, request, leader_id):
        if request.method == 'POST' and request.FILES.get('photo'):
            try:
                leader = Leadership.objects.get(id=leader_id)
                leader.image = request.FILES['photo']
                leader.save()
                messages.success(request, "Rahbar rasmi yuklandi!")
            except Exception as e:
                messages.error(request, f"Xato: {e}")
        return redirect('/admin/api/leadership/')

@admin.register(Department)
class DepartmentAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name_uz')