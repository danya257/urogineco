"""
Django settings for urogineco project — Beget hosting.
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'dev-only-insecure-key'
)

DEBUG = os.environ.get('DJANGO_DEBUG', '0') == '1'

ALLOWED_HOSTS = [
    'drgvozkc.beget.tech',
    'www.drgvozkc.beget.tech',
    '127.0.0.1',
    'localhost',
]

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'SAMEORIGIN'
SECURE_REFERRER_POLICY = 'same-origin'
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
# Secure-cookies включаются файлом-флагом HTTPS_ON рядом с manage.py, когда на домене заработает SSL
HTTPS_ON = (BASE_DIR / 'HTTPS_ON').exists()
SESSION_COOKIE_SECURE = HTTPS_ON
CSRF_COOKIE_SECURE = HTTPS_ON
CSRF_TRUSTED_ORIGINS = ['https://drgvozkc.beget.tech', 'http://drgvozkc.beget.tech']
# HSTS включим когда убедимся что HTTPS 100% работает
# SECURE_HSTS_SECONDS = 31536000
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'adminsortable2',
    'ckeditor',
    'ckeditor_uploader',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        # На проде без ManifestStorage — CKEditor кидает css без хешей и падает при collectstatic --clear
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage" if not DEBUG
                   else "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

ROOT_URLCONF = 'urogineco.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.site_globals',
            ],
        },
    },
]

WSGI_APPLICATION = 'urogineco.wsgi.application'

# Beget автоматически создал MySQL БД при установке Django
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', 'drgvozkc_dj1'),
        'USER': os.environ.get('DB_USER', 'drgvozkc_dj1'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '3306'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Static & Media
STATIC_URL = '/static/'
STATIC_ROOT = '/home/d/drgvozkc/drgvozkc.beget.tech/public_html/static'

MEDIA_URL = '/media/'
MEDIA_ROOT = '/home/d/drgvozkc/drgvozkc.beget.tech/public_html/media'

CKEDITOR_CONFIGS = {
    'minimal': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline'],
            ['NumberedList', 'BulletedList'],
            ['Link', 'Unlink'],
            ['RemoveFormat'],
        ],
        'height': 150,
        'width': '100%',
        'removePlugins': 'stylesheetparser',
        'allowedContent': True,
    },
    'default': {
        'toolbar': 'full',
        'height': 300,
        'width': '100%',
    },
}

CKEDITOR_UPLOAD_PATH = "uploads/"

# Оператор ПД (для страниц политики и согласия по 152-ФЗ)
OPERATOR_INFO = {
    'name': 'Гвоздев Михаил Юрьевич',
    'role': 'врач-урогинеколог',
    'address': '',
    'email': os.environ.get('OPERATOR_EMAIL', 'dr-gvozdev@mail.ru'),
    'phone': os.environ.get('OPERATOR_PHONE', ''),
    'site': 'https://drgvozkc.beget.tech',
    'privacy_updated': '14.09.2026',
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
        'file': {
            'class': 'logging.FileHandler',
            'filename': '/home/d/drgvozkc/drgvozkc.beget.tech/public_html/HelloDjango/HelloDjango/tmp/django.log',
            'formatter': 'verbose',
        },
    },
    'formatters': {
        'verbose': {
            'format': '{asctime} [{levelname}] {name}: {message}',
            'style': '{',
        },
    },
    'root': {'handlers': ['console']},
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console', 'file'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}
