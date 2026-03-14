import os, sys, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from docx import Document
from api.models import Employee
from django.conf import settings
from supabase import create_client

doc = Document('hodimlar.zip.docx')
supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

def get_cell_image(cell):
    for elem in cell._tc.iter():
        if elem.tag.endswith('}blip'):
            rId = elem.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
            if rId:
                try:
                    part = doc.part.related_parts[rId]
                    ext = part.content_type.split('/')[-1]
                    return part.blob, ext
                except:
                    pass
    return None, None

def clean_name(name):
    name = name.strip().split('\n')[0].strip()
    for s in [' й.', ' й', '  й.']:
        if s in name:
            name = name[:name.index(s)].strip()
    return name

# 1-ustun: ism, 2-ustun: rasm
pairs = []
for table in doc.tables:
    for row in table.rows:
        cells = row.cells
        if len(cells) >= 2:
            name = clean_name(cells[0].text)
            img_bytes, ext = get_cell_image(cells[1])
            if name and len(name) > 5 and 'Бўш' not in name and 'Фото' not in name and 'Ф.И.Ш' not in name:
                pairs.append((name, img_bytes, ext))

print(f"Word: {len(pairs)} jufti topildi")
for i, (n, img, ext) in enumerate(pairs[:5]):
    print(f"  {i+1}. {n} | rasm={'bor' if img else 'yoq'}")

def norm(n):
    n = n.strip().upper()
    for k, v in {'Ў':'У','ў':'у','Қ':'К','қ':'к','Ғ':'Г','ғ':'г','Ҳ':'Х','ҳ':'х','Ё':'Е','ё':'е','ъ':'','ь':''}.items():
        n = n.replace(k, v)
    return n

def fam_ism(n):
    p = n.strip().split()
    return norm(p[0]+' '+p[1]) if len(p)>=2 else norm(p[0]) if p else ''

def fam(n):
    p = n.strip().split()
    return norm(p[0]) if p else ''

employees = list(Employee.objects.all())
matched = 0
not_matched = []

for emp in employees:
    ru = emp.full_name_ru or ''
    best = None
    for name, img, ext in pairs:
        if img and fam_ism(name) == fam_ism(ru) and fam_ism(ru):
            best = (name, img, ext)
            break
    if not best:
        cands = [(n,i,e) for n,i,e in pairs if i and fam(n)==fam(ru) and fam(ru)]
        if len(cands) == 1:
            best = cands[0]
    if best:
        name, img, ext = best
        path = f"employees/employee_{emp.id}.{ext}"
        try:
            supabase.storage.from_(settings.SUPABASE_BUCKET).upload(path=path, file=img, file_options={"content-type": f"image/{ext}", "upsert": "true"})
            url = supabase.storage.from_(settings.SUPABASE_BUCKET).get_public_url(path)
            emp.image = url
            emp.save(update_fields=["image"])
            matched += 1
            print(f"OK ID={emp.id} {ru}")
        except Exception as e:
            print(f"XATO ID={emp.id}: {e}")
    else:
        not_matched.append(emp)

print(f"\nYuklandi: {matched}")
print(f"Topilmadi: {len(not_matched)}")
for emp in not_matched:
    print(f"  ID={emp.id} | {emp.full_name_ru}")