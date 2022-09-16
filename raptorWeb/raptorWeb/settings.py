"""
Django settings for the raptorWeb project.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from os.path import join
from os import getenv
from pathlib import Path
from dotenv import load_dotenv

# Project directories
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = join(BASE_DIR, "templates")
RAPTOMC_TEMPLATE_DIR = join(TEMPLATE_DIR, "raptormc")
APPLICATIONS_DIR = join(RAPTOMC_TEMPLATE_DIR, "applications")
STATIC_DIR = join(BASE_DIR, "static")
MEDIA_DIR = join(BASE_DIR, "media")

load_dotenv()

# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

with open(join(BASE_DIR, 'key.txt')) as key:

    SECRET_KEY =  key.read().strip()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['raptorapp', '127.0.0.1']

# Create superuser on new environments. To be changed immediately after creation
ADMINS = (
    ('sradmin', 'sradmin@shadowraptor.net'),
)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_bootstrap5',
    'ckeditor',
    'raptormc',
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
    'raptormc.jobs.RaptorWare',
]

ROOT_URLCONF = 'raptorWeb.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
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

WSGI_APPLICATION = 'raptorWeb.wsgi.application'
ASGI_APPLICATION = 'raptorWeb.asgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# Sqlite3 database for local development only

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': getenv('MYSQL_DATABASE'),
        'USER': getenv('MYSQL_USER'),
        'PASSWORD': getenv('MYSQL_PASSWORD'),
        'HOST': 'mariadb',
        'PORT': '3306',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 10,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Hashing algorithms

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = join(join(BASE_DIR, '..'), join('config', 'static'))

# THIS MUST BE NAMED `STATICFILES_DIRS`
STATICFILES_DIRS = [

    STATIC_DIR,

]

# Media files (User submitted content)

MEDIA_ROOT = MEDIA_DIR
MEDIA_URL = '/media/'

# Login URL

LOGIN_URL = 'raptormc/applications/login'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

BACKGROUND_TASK_RUN_ASYNC = True

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

SERVER_DATA = {
        "nomi": {
            "address": "nomi.shadowraptor.net",
            "port": 25566
        },
        "ob": {
            "address": "ob.shadowraptor.net",
            "port": 25567
        },
        "ftbu": {
            "address": "ftbu.shadowraptor.net",
            "port": 25568
        },
        "ct2": {
            "address": "ct2.shadowraptor.net",
            "port": 25569
        },
        "e6e": {
            "address": "e6e.shadowraptor.net",
            "port": 25570
        }
    }

BOOTSTRAP5 = {

    # Set placeholder attributes to label if no placeholder is provided.
    'set_placeholder': False,

}

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 450,
        'width': 1280,
    },
}
