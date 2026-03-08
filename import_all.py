import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

import openpyxl
from api.models import Department, Employee

Employee.objects.all().delete()
Department.objects.all().delete()
print('Baza tozalandi')

dept_wb = openpyxl.load_workbook('infakiosk_departments.xlsx')
dept_ws = dept_wb.active
dept_map = {}

for row in dept_ws.iter_rows(min_row=2, values_only=True):
    if not row[0]: continue
    name_uz = str(row[0]).strip()
    dept = Department.objects.create(name_uz=name_uz, name_ru=str(row[1]).strip() if row[1] else name_uz, name_en=str(row[2]).strip() if row[2] else name_uz)
    dept_map[name_uz] = dept

print(f'Bolimlar: {len(dept_map)} ta')
