import os, sys, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from api.models import Employee
from docx import Document

doc = Document('hodimlar.zip.docx')
word_names = []
for table in doc.tables:
    for row in table.rows:
        for cell in row.cells:
            text = cell.text.strip().split('\n')[0].strip()
            if (text and len(text) > 5 and not text.isdigit()
                and 'Ф.И.Ш' not in text and 'Фото' not in text
                and 'Бўш' not in text and 'Бош' not in text):
                word_names.append(text)

db_names = list(Employee.objects.all().order_by('id').values_list('id', 'full_name_ru'))

print(f"Word: {len(word_names)} nom")
print(f"DB:   {len(db_names)} hodim")
print()
print(f"{'DB ID':<6} {'DB ismi':<45} {'Word ismi'}")
print("-"*100)
for i, (emp_id, db_name) in enumerate(db_names):
    word_name = word_names[i] if i < len(word_names) else "---"
    match = "✓" if db_name and word_name and db_name.split()[0] == word_name.split()[0] else "✗"
    print(f"{emp_id:<6} {(db_name or ''):<45} {word_name}  {match}")