from django.contrib import admin
from django.utils.html import format_html
from django.urls import path
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from import_export.admin import ImportExportModelAdmin
from .models import Employee, Department, Leadership
from django.conf import settings
from supabase import create_client

supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY) if settings.SUPABASE_KEY else None


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
    list_display = ('full_name_uz', 'department', 'floor', 'room', 'photo_preview', 'upload_button')
    search_fields = ('full_name_uz', 'phone')
    list_filter = ('department', 'floor')

    def photo_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="60" style="object-fit:cover;border-radius:4px"/>', obj.image)
        return '—'
    photo_preview.short_description = 'Rasm'

    def upload_button(self, obj):
        return format_html(
            '<form method="post" enctype="multipart/form-data" action="/admin/api/employee/upload-photo/{}/" style="display:inline">'
            '<input type="hidden" name="csrfmiddlewaretoken" value="">'
            '<input type="file" name="photo" accept="image/*" style="font-size:11px;width:140px" '
            'onchange="this.previousElementSibling.value=document.cookie.match(/csrftoken=([^;]+)/)[1];this.form.submit()">'
            '</form>',
            obj.id
        )
    upload_button.short_description = 'Rasm yuklash'

    def get_urls(self):
        urls = super().get_urls()
        custom = [path('upload-photo/<int:employee_id>/', self.admin_site.admin_view(self.upload_photo_view))]
        return custom + urls

    def upload_photo_view(self, request, employee_id):
        from django.shortcuts import redirect
        if request.method == 'POST' and request.FILES.get('photo'):
            photo = request.FILES['photo']
            ext = photo.name.split('.')[-1].lower()
            path_str = f"employee_{employee_id}.{ext}"
            try:
                supabase.storage.from_(settings.SUPABASE_BUCKET).upload(
                    path=path_str, file=photo.read(),
                    file_options={"content-type": photo.content_type, "upsert": "true"}
                )
                url = supabase.storage.from_(settings.SUPABASE_BUCKET).get_public_url(path_str)
                Employee.objects.filter(id=employee_id).update(image=url)
                self.message_user(request, "Rasm yuklandi!")
            except Exception as e:
                self.message_user(request, f"Xato: {e}", level='error')
        return redirect('/admin/api/employee/')


@admin.register(Leadership)
class LeadershipAdmin(ImportExportModelAdmin):
    list_display = ('full_name_uz', 'position_uz', 'order', 'photo_preview', 'upload_button')
    list_editable = ('order',)
    search_fields = ('full_name_uz', 'position_uz')

    def photo_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="60" style="object-fit:cover;border-radius:4px"/>', obj.image)
        return '—'
    photo_preview.short_description = 'Rasm'

    def upload_button(self, obj):
        return format_html(
            '<form method="post" enctype="multipart/form-data" action="/admin/api/leadership/upload-leadership/{}/" style="display:inline">'
            '<input type="hidden" name="csrfmiddlewaretoken" value="">'
            '<input type="file" name="photo" accept="image/*" style="font-size:11px;width:140px" '
            'onchange="this.previousElementSibling.value=document.cookie.match(/csrftoken=([^;]+)/)[1];this.form.submit()">'
            '</form>',
            obj.id
        )
    upload_button.short_description = 'Rasm yuklash'

    def get_urls(self):
        urls = super().get_urls()
        custom = [path('upload-leadership/<int:leader_id>/', self.admin_site.admin_view(self.upload_photo_view))]
        return custom + urls

    def upload_photo_view(self, request, leader_id):
        from django.shortcuts import redirect
        if request.method == 'POST' and request.FILES.get('photo'):
            photo = request.FILES['photo']
            ext = photo.name.split('.')[-1].lower()
            path_str = f"leadership_{leader_id}.{ext}"
            try:
                supabase.storage.from_(settings.SUPABASE_BUCKET).upload(
                    path=path_str, file=photo.read(),
                    file_options={"content-type": photo.content_type, "upsert": "true"}
                )
                url = supabase.storage.from_(settings.SUPABASE_BUCKET).get_public_url(path_str)
                Leadership.objects.filter(id=leader_id).update(image=url)
                self.message_user(request, "Rasm yuklandi!")
            except Exception as e:
                self.message_user(request, f"Xato: {e}", level='error')
        return redirect('/admin/api/leadership/')


@admin.register(Department)
class DepartmentAdmin(ImportExportModelAdmin):
    list_display = ('name_uz', 'name_ru', 'name_en')