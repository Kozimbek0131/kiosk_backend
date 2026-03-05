import os
from pathlib import Path

# Loyihaning asosiy yo'li
BASE_DIR = Path(__file__).resolve().parent.parent

# Xavfsizlik kaliti
SECRET_KEY = 'django-insecure-your-key-here'

# Debug rejimi (Production uchun True qolishi mumkin, lekin ehtiyot bo'ling)
DEBUG = True

# Ruxsat berilgan hostlar
ALLOWED_HOSTS = [
    'web-production-ba75.up.railway.app', 
    '127.0.0.1', 
    'localhost',
    '*'
]

# Ilovalar ro'yxati
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Qo'shimcha kutubxonalar
    'rest_framework',
    'corsheaders',
    'api',
]

# Middleware sozlamalari (Tartib juda muhim!)
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', # CORS har doim eng tepada bo'lishi shart
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Statik fayllar uchun
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Ma'lumotlar bazasi (Railway-da SQLite ishlatilyapti)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# --- CORS va CSRF SOZLAMALARI (Frontend uchun muhim) ---
CORS_ALLOW_ALL_ORIGINS = True # Barcha frontend so'rovlariga ruxsat berish

CSRF_TRUSTED_ORIGINS = [
    'https://web-production-ba75.up.railway.app',
    'https://akadeyima-kiosk.vercel.app', # Vercel-dagi asosiy manzilingiz
    'https://akademiya-kiosk.vercel.app'
]

# --- Til va vaqt ---
LANGUAGE_CODE = 'uz-uz'
TIME_ZONE = 'Asia/Tashkent'
USE_I18N = True
USE_TZ = True

# --- Statik va Media fayllar ---
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# WhiteNoise statik fayllarni siqish va keshlashen uchun
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media fayllar (Xodimlar rasmlari uchun)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'