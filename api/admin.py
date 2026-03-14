import time
from django.contrib import admin
from django.utils.html import format_html
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from import_export.admin import ImportExportModelAdmin
from .models import Employee, Department, Leadership
from django.conf import settings
from django.shortcuts import redirect

# Supabase ulanishini xavfsiz qilish
try:
    from supabase import create_client
    # Settingsda kalitlar borligini tekshiramiz
    supabase_url = getattr(settings, 'SUPABASE_URL', None)
    supabase_key = getattr(settings, 'SUPABASE_KEY', None)
    
    if supabase_url and supabase_key:
        supabase = create_client(supabase_url, supabase_key)
    else:
        supabase = None
except Exception:
    supabase = None

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
    readonly_fields = ('photo_preview',)

    def photo_preview(self, obj):
        if obj.image:
            # Agar URL bo'lsa string sifatida, agar fayl bo'lsa .url sifatida oladi
            img_url = obj.image.url if hasattr(obj.image, 'url') else obj.image
            return format_html('<img src="{}" width="60" height="75" style="object-fit:cover;border-radius:4px"/>', img_url)
        return '—'
    photo_preview.short_description = 'Rasm'

    def upload_button(self, obj):
        # Action yo'lini tekshiring: /admin/api/employee/... loyihangiz papka nomiga mosmi?
        return format_html(
            '<form method="post" enctype="multipart/form-data" '
            'action="/admin/api/employee/upload-photo/{}/" style="display:inline">'
            '<input type="file" name="photo" accept="image/*" style="font-size:10px;width:130px" '
            'onchange="this.form.submit()">'
            '</form>',
            obj.id
        )
    upload_button.short_description = 'Tezkor yuklash'

    def get_urls(self):
        urls = super().get_urls()
        custom = [path('upload-photo/<int:employee_id>/',
                        csrf_exempt(self.admin_site.admin_view(self.upload_photo_view)))]
        return custom + urls

    def upload_photo_view(self, request, employee_id):
        if request.method == 'POST' and request.FILES.get('photo'):
            if not supabase:
                self.message_user(request, "Xato: Supabase ulanmagan! Settings faylni tekshiring.", level='error')
                return redirect('/admin/api/employee/')

            photo = request.FILES['photo']
            ext = photo.name.split('.')[-1].lower()
            path_str = f"employees/emp_{employee_id}_{int(time.time())}.{ext}"
            
            try:
                # Faylni o'qish
                file_content = photo.read()
                
                # Supabasega yuklash
                supabase.storage.from_(settings.SUPABASE_BUCKET).upload(
                    path=path_str, 
                    file=file_content,
                    file_options={"content-type": photo.content_type, "upsert": "true"}
                )
                
                # Public URL olish
                url = supabase.storage.from_(settings.SUPABASE_BUCKET).get_public_url(path_str)
                
                # Bazani yangilash
                Employee.objects.filter(id=employee_id).update(image=url)
                self.message_user(request, f"Rasm yuklandi: {path_str}")
                
            except Exception as e:
                self.message_user(request, f"Yuklashda xato: {str(e)}", level='error')
        else:
            self.message_user(request, "Fayl tanlanmadi yoki noto'g'ri so'rov.", level='warning')
            
        return redirect('/admin/api/employee/')

# Leadership qismini ham xuddi shunday redirect va message bilan yangilang...
@admin.register(Leadership)
class LeadershipAdmin(ImportExportModelAdmin):
    list_display = ('full_name_uz', 'position_uz', 'order', 'photo_preview', 'upload_button')
    list_editable = ('order',)
    readonly_fields = ('photo_preview',)
    
    def photo_preview(self, obj):
        if obj.image:
            img_url = obj.image.url if hasattr(obj.image, 'url') else obj.image
            return format_html('<img src="{}" width="60" height="75" style="object-fit:cover;border-radius:4px"/>', img_url)
        return '—'

    def upload_button(self, obj):
        return format_html(
            '<form method="post" enctype="multipart/form-data" '
            'action="/admin/api/leadership/upload-leadership/{}/" style="display:inline">'
            '<input type="file" name="photo" accept="image/*" style="font-size:10px;width:130px" '
            'onchange="this.form.submit()">'
            '</form>',
            obj.id
        )

    def get_urls(self):
        urls = super().get_urls()
        custom = [path('upload-leadership/<int:leader_id>/',
                        csrf_exempt(self.admin_site.admin_view(self.upload_leadership_photo_view)))]
        return custom + urls

    def upload_leadership_photo_view(self, request, leader_id):
        if request.method == 'POST' and request.FILES.get('photo'):
            if not supabase:
                self.message_user(request, "Xato: Supabase ulanmagan!", level='error')
                return redirect('/admin/api/leadership/')
                
            photo = request.FILES['photo']
            ext = photo.name.split('.')[-1].lower()
            path_str = f"leadership/lead_{leader_id}_{int(time.time())}.{ext}"
            try:
                supabase.storage.from_(settings.SUPABASE_BUCKET).upload(
                    path=path_str, file=photo.read(),
                    file_options={"content-type": photo.content_type, "upsert": "true"}
                )
                url = supabase.storage.from_(settings.SUPABASE_BUCKET).get_public_url(path_str)
                Leadership.objects.filter(id=leader_id).update(image=url)
                self.message_user(request, "Rahbar rasmi yuklandi!")
            except Exception as e:
                self.message_user(request, f"Xato: {e}", level='error')
        return redirect('/admin/api/leadership/')

@admin.register(Department)
class DepartmentAdmin(ImportExportModelAdmin):
    list_display = ('name_uz', 'name_ru', 'name_en')