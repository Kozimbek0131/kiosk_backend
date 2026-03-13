import time
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


def get_upload_js():
    return """
<script>
function uploadPhoto(input, url) {
    var token = null;
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
        var c = cookies[i].trim();
        if (c.startsWith('csrftoken=')) {
            token = c.substring('csrftoken='.length);
            break;
        }
    }
    if (!token) {
        var el = document.querySelector('[name=csrfmiddlewaretoken]');
        if (el) token = el.value;
    }
    if (!token) { alert('CSRF token topilmadi!'); return; }
    var f = new FormData();
    f.append('photo', input.files[0]);
    f.append('csrfmiddlewaretoken', token);
    fetch(url, {method: 'POST', body: f})
        .then(function(r){ return r.json(); })
        .then(function(d){ if(d.success){ location.reload(); } else { alert('Xato: ' + d.error); } })
        .catch(function(e){ alert('Xato: ' + e); });
}
</script>
"""


@admin.register(Employee)
class EmployeeAdmin(ImportExportModelAdmin):
    resource_class = EmployeeResource
    list_display = ('full_name_uz', 'department', 'floor', 'room', 'photo_preview', 'upload_button')
    search_fields = ('full_name_uz', 'phone')
    list_filter = ('department', 'floor')
    readonly_fields = ('photo_preview',)
    fields = ('full_name_uz', 'full_name_ru', 'full_name_en',
              'position_uz', 'position_ru', 'position_en',
              'department', 'floor', 'room', 'phone', 'image', 'photo_preview')

    def photo_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="120" style="object-fit:cover;border-radius:4px"/>', obj.image)
        return '—'
    photo_preview.short_description = 'Joriy rasm'

    def upload_button(self, obj):
        js = get_upload_js()
        return format_html(
            '{}<input type="file" name="photo" accept="image/*" style="font-size:11px;width:140px" '
            'onchange="uploadPhoto(this, \'/admin/api/employee/upload-photo/{}/\')">',
            js, obj.id
        )
    upload_button.short_description = 'Rasm yuklash'

    def get_urls(self):
        urls = super().get_urls()
        custom = [path('upload-photo/<int:employee_id>/', self.admin_site.admin_view(self.upload_photo_view))]
        return custom + urls

    def upload_photo_view(self, request, employee_id):
        from django.http import JsonResponse
        if request.method == 'POST' and request.FILES.get('photo'):
            photo = request.FILES['photo']
            ext = photo.name.split('.')[-1].lower()
            path_str = f"employee_{employee_id}_{int(time.time())}.{ext}"
            try:
                supabase.storage.from_(settings.SUPABASE_BUCKET).upload(
                    path=path_str, file=photo.read(),
                    file_options={"content-type": photo.content_type, "upsert": "true"}
                )
                url = supabase.storage.from_(settings.SUPABASE_BUCKET).get_public_url(path_str)
                Employee.objects.filter(id=employee_id).update(image=url)
                return JsonResponse({"success": True, "url": url})
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)
        return JsonResponse({"error": "No file"}, status=400)


@admin.register(Leadership)
class LeadershipAdmin(ImportExportModelAdmin):
    list_display = ('full_name_uz', 'position_uz', 'order', 'photo_preview', 'upload_button')
    list_editable = ('order',)
    search_fields = ('full_name_uz', 'position_uz')
    readonly_fields = ('photo_preview',)
    fields = ('full_name_uz', 'full_name_ru', 'full_name_en',
              'position_uz', 'position_ru', 'position_en',
              'order', 'image', 'photo_preview')

    def photo_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="120" style="object-fit:cover;border-radius:4px"/>', obj.image)
        return '—'
    photo_preview.short_description = 'Joriy rasm'

    def upload_button(self, obj):
        js = get_upload_js()
        return format_html(
            '{}<input type="file" name="photo" accept="image/*" style="font-size:11px;width:140px" '
            'onchange="uploadPhoto(this, \'/admin/api/leadership/upload-leadership/{}/\')">',
            js, obj.id
        )
    upload_button.short_description = 'Rasm yuklash'

    def get_urls(self):
        urls = super().get_urls()
        custom = [path('upload-leadership/<int:leader_id>/', self.admin_site.admin_view(self.upload_photo_view))]
        return custom + urls

    def upload_photo_view(self, request, leader_id):
        from django.http import JsonResponse
        if request.method == 'POST' and request.FILES.get('photo'):
            photo = request.FILES['photo']
            ext = photo.name.split('.')[-1].lower()
            path_str = f"leadership_{leader_id}_{int(time.time())}.{ext}"
            try:
                supabase.storage.from_(settings.SUPABASE_BUCKET).upload(
                    path=path_str, file=photo.read(),
                    file_options={"content-type": photo.content_type, "upsert": "true"}
                )
                url = supabase.storage.from_(settings.SUPABASE_BUCKET).get_public_url(path_str)
                Leadership.objects.filter(id=leader_id).update(image=url)
                return JsonResponse({"success": True, "url": url})
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)
        return JsonResponse({"error": "No file"}, status=400)


@admin.register(Department)
class DepartmentAdmin(ImportExportModelAdmin):
    list_display = ('name_uz', 'name_ru', 'name_en')