from django.db import models
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
import os
import requests
import mimetypes
import uuid

@deconstructible
class SupabaseStorage(Storage):
    def __init__(self):
        self.supabase_url = os.environ.get('SUPABASE_URL', 'https://ywqrlfufkrdokpbdodav.supabase.co').rstrip('/')
        self.supabase_key = os.environ.get('SUPABASE_KEY', '')
        self.bucket = 'employees'

    def _save(self, name, content):
        ext = name.split('.')[-1]
        safe_name = f"{uuid.uuid4()}.{ext}"
        
        folder = os.path.dirname(name)
        clean_name = os.path.basename(safe_name)
        path_on_supabase = f"{folder}/{clean_name}" if folder else clean_name

        upload_url = f"{self.supabase_url}/storage/v1/object/{self.bucket}/{path_on_supabase}"
        
        content_type, _ = mimetypes.guess_type(name)
        headers = {
            'Authorization': f'Bearer {self.supabase_key}',
            'Content-Type': content_type or 'image/jpeg',
            'x-upsert': 'true'
        }
        
        content.seek(0)
        try:
            response = requests.put(upload_url, headers=headers, data=content.read(), timeout=15)
            if response.status_code not in (200, 201):
                return name
        except Exception:
            return name
            
        return path_on_supabase

    def url(self, name):
        if not name:
            return None
        if str(name).startswith('http'):
            return str(name)
        return f"{self.supabase_url}/storage/v1/object/public/{self.bucket}/{name}"

    def exists(self, name):
        return False

    def delete(self, name):
        requests.delete(
            f"{self.supabase_url}/storage/v1/object/{self.bucket}/{name}",
            headers={'Authorization': f'Bearer {self.supabase_key}'}
        )

supabase_storage = SupabaseStorage()

# --- Modellar ---

class Department(models.Model):
    name_uz = models.CharField("Bo'lim nomi (UZ)", max_length=255)
    name_ru = models.CharField("Название (RU)", max_length=255)
    name_en = models.CharField("Department Name (EN)", max_length=255)
    order = models.PositiveIntegerField("Bo'lim tartibi", default=100)

    class Meta:
        verbose_name = "Bo'lim"
        verbose_name_plural = "Bo'limlar"
        ordering = ['order', 'name_uz']

    def __str__(self):
        return self.name_uz

class Employee(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='employees')
    full_name_uz = models.CharField("F.I.SH (UZ)", max_length=255)
    full_name_ru = models.CharField("Ф.И.О (RU)", max_length=255)
    full_name_en = models.CharField("Full Name (EN)", max_length=255)
    position_uz = models.CharField("Lavozimi (UZ)", max_length=255)
    position_ru = models.CharField("Должность (RU)", max_length=255)
    position_en = models.CharField("Position (EN)", max_length=255)
    
    floor = models.CharField("Qavat", max_length=10, blank=True, null=True)
    room = models.CharField("Xona", max_length=10, blank=True, null=True)
    phone = models.CharField("Telefon", max_length=20, blank=True, null=True)
    image = models.ImageField(
        "Rasm",
        storage=supabase_storage,
        upload_to='employees',
        blank=True,
        null=True
    )
    order = models.PositiveIntegerField("Bo'lim ichidagi tartib", default=100)

    class Meta:
        verbose_name = "Xodim"
        verbose_name_plural = "Xodimlar"
        ordering = ['department__order', 'order', 'full_name_uz']

    def __str__(self):
        return self.full_name_uz

class Leadership(models.Model):
    # Unvonlar uchun variantlar
    RANK_CHOICES = [
        ('Adliya katta maslahatchisi', 'Adliya katta maslahatchisi'),
        ('Adliya maslahatchisi', 'Adliya maslahatchisi'),
        ('Adliya general-mayori', 'Adliya general-mayori'),
        ('1-darajali adliya maslahatchisi', '1-darajali adliya maslahatchisi'),
        ('2-darajali adliya maslahatchisi', '2-darajali adliya maslahatchisi'),
    ]

    full_name_uz = models.CharField("F.I.SH (UZ)", max_length=255)
    full_name_ru = models.CharField("Ф.И.О (RU)", max_length=255, blank=True, null=True)
    full_name_en = models.CharField("Full Name (EN)", max_length=255, blank=True, null=True)
    
    # UNVON MAYDONLARI (Admin panel qidirayotgan maydonlar)
    rank_uz = models.CharField("Unvoni (UZ)", max_length=100, choices=RANK_CHOICES, default='Adliya katta maslahatchisi')
    rank_ru = models.CharField("Звание (RU)", max_length=100, default='Старший советник юстиции')
    rank_en = models.CharField("Rank (EN)", max_length=100, default='Senior Justice Advisor')

    position_uz = models.CharField("Lavozimi (UZ)", max_length=255, blank=True, null=True)
    position_ru = models.CharField("Должность (RU)", max_length=255, blank=True, null=True)
    position_en = models.CharField("Position (EN)", max_length=255, blank=True, null=True)
    
    # ALOQA MAYDONLARI
    phone = models.CharField("Telefon", max_length=25, default="+998712020496")
    email = models.EmailField("Email", default="info@proacademy.uz")
    work_hours_uz = models.CharField("Ish vaqti (UZ)", max_length=100, default="Har ish kuni 09:00-18:00")
    work_hours_ru = models.CharField("График работы (RU)", max_length=100, default="Каждый рабочий день 09:00-18:00")

    image = models.ImageField(
        "Rasm",
        storage=supabase_storage,
        upload_to='leadership',
        blank=True,
        null=True
    )
    order = models.PositiveIntegerField("Tartib raqami", default=0)

    class Meta:
        verbose_name = "Rahbariyat"
        verbose_name_plural = "Rahbariyat"
        ordering = ['order']

    def __str__(self):
        return self.full_name_uz