from django.db import models
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
import os
import requests
import mimetypes # Dinamik Content-Type uchun

@deconstructible
class SupabaseStorage(Storage):
    def __init__(self):
        # Settings dan olish xavfsizroq, lekin environ ham bo'laveradi
        self.supabase_url = os.environ.get('SUPABASE_URL', 'https://ywqrlfufkrdokpbdodav.supabase.co')
        self.supabase_key = os.environ.get('SUPABASE_KEY', '')
        self.bucket = 'employees'

    def _save(self, name, content):
        upload_url = f"{self.supabase_url}/storage/v1/object/{self.bucket}/{name}"
        
        # Dinamik ravishda fayl turini aniqlash (jpeg, png, webp)
        content_type, _ = mimetypes.guess_type(name)
        if not content_type:
            content_type = 'image/jpeg'

        headers = {
            'Authorization': f'Bearer {self.supabase_key}',
            'Content-Type': content_type,
            'x-upsert': 'true'
        }
        
        content.seek(0)
        # PUT so'rovi bilan faylni yuborish
        response = requests.put(upload_url, headers=headers, data=content.read())
        
        if response.status_code not in (200, 201):
            # Xatoni terminalda va logda ko'rish uchun
            print(f"DEBUG: Supabase error - {response.text}")
            raise Exception(f"Supabase upload xatosi: {response.text}")
        
        return name

    def url(self, name):
        if not name:
            return None
        if str(name).startswith('http'):
            return str(name)
        # Public URL qaytarish
        return f"{self.supabase_url}/storage/v1/object/public/{self.bucket}/{name}"

    def exists(self, name):
        return False # Har doim yangi fayl deb hisoblash (upsert:true borligi uchun)

    def delete(self, name):
        requests.delete(
            f"{self.supabase_url}/storage/v1/object/{self.bucket}/{name}",
            headers={'Authorization': f'Bearer {self.supabase_key}'}
        )

supabase_storage = SupabaseStorage()

# --- Modellar qismi (O'zgarishsiz qolishi mumkin, lekin blank=True borligiga ishonch hosil qiling) ---

class Department(models.Model):
    name_uz = models.CharField("Bo'lim nomi (UZ)", max_length=255)
    name_ru = models.CharField("Название (RU)", max_length=255)
    name_en = models.CharField("Department Name (EN)", max_length=255)

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
    floor = models.CharField("Qavat", max_length=10)
    room = models.CharField("Xona", max_length=10)
    phone = models.CharField("Telefon", max_length=20, blank=True, null=True)
    image = models.ImageField(
        "Rasm",
        storage=supabase_storage,
        upload_to='employees/',
        blank=True, # Majburiy emas
        null=True   # Majburiy emas
    )

    def __str__(self):
        return self.full_name_uz

class Leadership(models.Model):
    full_name_uz = models.CharField("F.I.SH (UZ)", max_length=255)
    # ... boshqa maydonlar ...
    image = models.ImageField(
        "Rasm",
        storage=supabase_storage,
        upload_to='leadership/',
        blank=True,
        null=True
    )
    order = models.IntegerField("Tartib raqami", default=0)
    # ... qolgan qismi ...