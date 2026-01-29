import os
from pathlib import Path

# -------------------------------
# Base directory
# -------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------------------
# Security
# -------------------------------
SECRET_KEY = 'django-insecure-s)dynxv&m7!4j8eap($rm^quqda&_9&d+%8prpo^0_eaku!1=t'
DEBUG = True
ALLOWED_HOSTS = ["*"]

# -------------------------------
# Applications
# -------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Project apps
    'main',

    # Third-party
    'rest_framework',
    'django_filters',
    'drf_spectacular',
    'corsheaders',
]

# -------------------------------
# Middleware
# -------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "corsheaders.middleware.CorsMiddleware",
]

CORS_ALLOW_ALL_ORIGINS = True


# -------------------------------
# URLs and WSGI
# -------------------------------
ROOT_URLCONF = 'root.urls'
WSGI_APPLICATION = 'root.wsgi.application'

# -------------------------------
# Templates
# -------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

# -------------------------------
# Database (SQLite)
# -------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'hotel_db',
        'USER': 'postgres',
        'PASSWORD': '1',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# -------------------------------
# Password validation
# -------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# -------------------------------
# Internationalization
# -------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Tashkent'
USE_I18N = True
USE_TZ = True

# -------------------------------
# Static files (CSS, JS, etc.)
# -------------------------------
STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / "staticfiles"  # collectstatic qilinganda fayllar shu yerga tushadi

# -------------------------------
# Media files (rasmlar, fayllar)
# -------------------------------
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"

# -------------------------------
# Django REST Framework
# -------------------------------
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# -------------------------------
# drf-spectacular (API dokumentatsiya)
# -------------------------------
SPECTACULAR_SETTINGS = {
    'TITLE': 'Hotel Location',
    'DESCRIPTION': 'Foydalanish uchun juda qulay',
    'VERSION': '1.0.0',
}

# settings.py
CSRF_TRUSTED_ORIGINS = [
    'https://berniece-unincluded-liane.ngrok-free.dev',
]
