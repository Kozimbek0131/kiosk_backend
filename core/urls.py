from django.contrib import admin
from django.urls import path, include # include qo'shildi
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # MANA SHU QATORNI ALBATTA QO'SHING:
    path('api/', include('api.urls')), 
]

# Rasm va statik fayllar uchun (Production va Debug rejimlari uchun)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)