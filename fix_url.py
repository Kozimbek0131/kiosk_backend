import os, sys, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()
from api.models import Employee
count = 0
for e in Employee.objects.all():
    if e.image and 'employees/employees/' in str(e.image):
        e.image = str(e.image).replace('employees/employees/', 'employees/')
        e.save(update_fields=['image'])
        count += 1
print(f'Tuzatildi: {count}')
print(Employee.objects.get(id=2).image)