import time
from django.contrib import admin
from django.utils.html import format_html
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from .models import Employee, Department, Leadership
from django.contrib import messages

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    # Admin ro'yxatida ko'rinadigan ustunlar
    list_display = ('full_name_uz', 'department', 'floor', 'room', 'photo_preview', 'upload_button')
    search_fields = ('full_name_uz', 'phone')
    
    # Rasmning ko'rinishi
    def photo_preview(self, obj):
        if obj.image:
            # Sizning url() metodiz ishga tushadi
            return format_html('<img src="{}" width="60" height="75" style="object-fit:cover;border-radius:4px"/>', obj.image.url)
        return '—'
    photo_preview.short_description = 'Rasm'

    # Tezkor yuklash tugmasi
    def upload_button(self, obj):
        return format_html(
            '<form method="post" enctype="multipart/form-data" action="/admin/api/employee/upload-photo/{}/">'
            '<input type="file" name="photo" accept="image/*" style="font-size:10px;width:130px" onchange="this.form.submit()">'
            '</form>',
            obj.id
        )
    upload_button.short_description = 'Tezkor yuklash'

    def get_urls(self):
        urls = super().get_urls()
        custom = [path('upload-photo/<int:employee_id>/', csrf_exempt(self.admin_site.admin_view(self.upload_photo_view)))]
        return custom + urls

    def upload_photo_view(self, request, employee_id):
        if request.method == 'POST' and request.FILES.get('photo'):
            try:
                employee = Employee.objects.get(id=employee_id)
                photo = request.FILES['photo']
                
                # SIZNING MODELINGIZDAGI IMAGEFIELD ISHGA TUSHADI
                # Bu avtomatik SupabaseStorage._save() metodini chaqiradi
                employee.image = photo
                employee.save()
                
                messages.success(request, f"{employee.full_name_uz} uchun rasm Supabasega yuklandi!")
            except Exception as e:
                messages.error(request, f"Xatolik: {str(e)}")
        return redirect('/admin/api/employee/')

@admin.register(Leadership)
class LeadershipAdmin(admin.ModelAdmin):
    list_display = ('full_name_uz', 'position_uz', 'order', 'photo_preview', 'upload_button')
    list_editable = ('order',)

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
                messages.success(request, "Rahbar rasmi yangilandi!")
            except Exception as e:
                messages.error(request, f"Xato: {e}")
        return redirect('/admin/api/leadership/')

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name_uz', 'name_ru', 'name_en')