from django.db import models

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
    image = models.URLField("Rasm URL", max_length=500, blank=True, null=True)

    def __str__(self):
        return self.full_name_uz

class Leadership(models.Model):
    full_name_uz = models.CharField("F.I.SH (UZ)", max_length=255)
    full_name_ru = models.CharField("Ф.И.О (RU)", max_length=255, blank=True, null=True)
    full_name_en = models.CharField("Full Name (EN)", max_length=255, blank=True, null=True)
    position_uz = models.CharField("Lavozimi (UZ)", max_length=255)
    position_ru = models.CharField("Должность (RU)", max_length=255, blank=True, null=True)
    position_en = models.CharField("Position (EN)", max_length=255, blank=True, null=True)
    rank_uz = models.CharField("Darajasi (UZ)", max_length=255, blank=True, null=True)
    rank_ru = models.CharField("Звание (RU)", max_length=255, blank=True, null=True)
    rank_en = models.CharField("Rank (EN)", max_length=255, blank=True, null=True)
    image = models.URLField("Rasm URL", max_length=500, blank=True, null=True)
    order = models.IntegerField("Tartib raqami", default=0)

    class Meta:
        verbose_name = "Rahbariyat"
        verbose_name_plural = "Rahbariyat"
        ordering = ['order']

    def __str__(self):
        return self.full_name_uz