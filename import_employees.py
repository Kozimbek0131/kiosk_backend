import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

import openpyxl
from api.models import Department, Employee

dept_map = {d.name_uz: d for d in Department.objects.all()}
print('Bolimlar topildi:', len(dept_map))

emp_wb = openpyxl.load_workbook('infakiosk_hodimlar.xlsx')
emp_ws = emp_wb.active
success, errors, not_found = 0, 0, set()

def s(v):
    if v is None: return ''
    if isinstance(v, float): v = int(v)
    return str(v).strip()

for row in emp_ws.iter_rows(min_row=2, values_only=True):
    try:
        _, n_uz, n_ru, n_en, p_uz, p_ru, p_en, dept_name, floor, room, ph1, ph2 = row
        if not dept_name: continue
        dept = dept_map.get(s(dept_name))
        if not dept:
            for k in dept_map:
                if s(dept_name).lower() in k.lower() or k.lower() in s(dept_name).lower():
                    dept = dept_map[k]
                    break
        if not dept:
            not_found.add(s(dept_name))
            errors += 1
            continue
        Employee.objects.create(department=dept, full_name_uz=s(n_uz) or 'Noma''lum', full_name_ru=s(n_ru) or s(n_uz), full_name_en=s(n_en) or s(n_uz), position_uz=s(p_uz), position_ru=s(p_ru) or s(p_uz), position_en=s(p_en) or s(p_uz), floor=s(floor), room=s(room), phone=s(ph2) or s(ph1))
        success += 1
    except Exception as e:
        print(f'Xato: {e}')
        errors += 1

print(f'Xodimlar: {success} ta yuklandi')
print(f'Xatolar: {errors} ta')
if not_found: print(f'Topilmagan bolimlar: {not_found}')
