import os
from pathlib import Path
from dotenv import load_dotenv


# Set the project root directory.
BASE_DIR = Path(__file__).resolve().parent.parent


# Load environment variables if running locally.
if not os.getenv('IS_DOCKER'):
    # 'IS_DOCKER' will exist only if running in Docker.
    # WARNING: If running locally, SQLite will be used.
    env_path = BASE_DIR / '../../infra/.env'
    load_dotenv(env_path)


# Main settings.
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS').split()
DEBUG = os.getenv('DJANGO_DEBUG', 'True') == 'True'


# Application definition.
INSTALLED_APPS = [
    # Django.
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party.
    'rest_framework',            # API Framework.
    'rest_framework.authtoken',  # Auth Token.
    'django_filters',            # Filters in API.
    'djoser',                    # Authentication Framework.
    'corsheaders',               # CORS.

    # Local.
    'users.apps.UsersConfig',
    'recipes.apps.RecipesConfig',
    'api.apps.ApiConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # CORS.
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'foodgram.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'foodgram.wsgi.application'


# Database definition.
# Set up PSQL if running in Docker else use SQLite.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'django'),
        'USER': os.getenv('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'postgres'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432')
    }
} if os.getenv('IS_DOCKER') else {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Authentication.
AUTH_USER_MODEL = 'users.CustomUser'
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


# Internationalization.
LANGUAGE_CODE = 'ru-RU'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images).
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media/'


# Default primary key field type.
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# REST API & Djoser definition.
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.UserRateThrottle',
        'rest_framework.throttling.AnonRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'user': '1000/hour',
        'anon': '200/hour',
    },
    'DEFAULT_PAGINATION_CLASS': 'api.v1.pagination.PageNumberSizedPagination',
    'PAGE_SIZE': 6,
}
DJOSER = {
    'LOGIN_FIELD': 'email',
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION': False,
    # It'd be better to set True, but the specification is the specification.
    # 'USER_CREATE_PASSWORD_RETYPE': True,
    # 'SET_PASSWORD_RETYPE': True,
    'HIDE_USERS': False,  # If true, `user_list` will return only CurrentUser.
    'SEND_ACTIVATION_EMAIL': False,
    'SERIALIZERS': {
        'user': 'api.v1.serializers.users.CustomUserSerializer',
        'current_user': 'api.v1.serializers.users.CustomUserSerializer',
        'user_create': 'api.v1.serializers.users.CustomUserCreateSerializer',
    },
    'PERMISSIONS': {
        'user': ['rest_framework.permissions.IsAuthenticatedOrReadOnly'],
        'user_list': ['rest_framework.permissions.AllowAny'],
    },
}

# CORS allowed origins definition.
CORS_ALLOWED_ORIGINS = os.getenv('DJANGO_CORS_ALLOWED_ORIGINS', '').split()
