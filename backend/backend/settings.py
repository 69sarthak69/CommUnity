import os
import environ
from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

# Initialize environment variables
env = environ.Env()
env.read_env(os.path.join(BASE_DIR, '.env'))  # Explicitly load .env file

# Database connection using DATABASE_URL
DATABASES = {
    'default': env.db('DATABASE_URL', default='postgres://postgres:admin@localhost:5432/community_platform')
}

# Secret key
SECRET_KEY = env('SECRET_KEY', default='fallback-secret-key')

# Quick-start development settings - unsuitable for production
DEBUG = True
ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'accounts',
    'corsheaders',
    'help_requests',
    'groups',
    'events',
    'notifications',
    'channels',
    'chat',
    'donation',
    
]

KHALTI_SECRET_KEY = "test_secret_key_18d538e7c1de4a528b974a05a6548a04"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',  # This is for your Django templates, not Vue.js
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

# Add the path to your Vue.js dist folder and other static assets
STATICFILES_DIRS = [
    "C:/Users/Sarthak Shrestha/Desktop/FYP_COMMUNITY_PLATFORM/frontend/dist/assets",
]


# Set the STATIC_ROOT for `collectstatic` to gather files
STATIC_ROOT = BASE_DIR / "staticfiles"  # This is where all static files will be collected

if DEBUG:
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',  # Allow public access
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}


# Custom User Model
AUTH_USER_MODEL = 'accounts.CustomUser'

CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Your Vue.js frontend
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # Default backend
]

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),  # Token expires in 60 mins
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),  # Refresh token expires in 7 days
    'ROTATE_REFRESH_TOKENS': True,  # Generates a new refresh token on refresh
    'BLACKLIST_AFTER_ROTATION': True,  # Blacklist old refresh tokens after refresh
    'ALGORITHM': 'HS256',  # Hashing algorithm
    'SIGNING_KEY': SECRET_KEY,  # Uses your Django secret key
    'AUTH_HEADER_TYPES': ('Bearer',),  # Must use 'Bearer <token>' in requests
}

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


ASGI_APPLICATION = 'backend.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}