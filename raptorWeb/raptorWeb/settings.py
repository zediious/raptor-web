from os.path import join
from os import getenv
from pathlib import Path
from dotenv import load_dotenv

# Define project directories
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = join(BASE_DIR, "templates")
STATIC_DIR = join(BASE_DIR, "static")
MEDIA_DIR = join(BASE_DIR, "media")

RAPTOMC_TEMPLATE_DIR = join(TEMPLATE_DIR, "raptormc")
APPLICATIONS_DIR = join(RAPTOMC_TEMPLATE_DIR, "applications")
PROFILES_DIR = join(RAPTOMC_TEMPLATE_DIR, 'profiles')

GAMESERVERS_TEMPLATE_DIR = join(TEMPLATE_DIR, 'gameservers')
STAFFAPPS_TEMPLATE_DIR = join(TEMPLATE_DIR, 'staffapps')
AUTH_TEMPLATE_DIR = join(TEMPLATE_DIR, 'authprofiles')

# Load .env file
load_dotenv()

# Load key.txt for Django secret key
with open(join(BASE_DIR, 'key.txt')) as key:

    SECRET_KEY =  key.read().strip()

# CSRF
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# SECURITY WARNING: Neither of the below two True in production!
DEBUG = True
USE_SQLITE = True

# Configure "DOMAIN_NAME" to match the domain name you will use (no www)
DOMAIN_NAME = "shadowraptor.net"

# Configure web protocol based on DEBUG status
WEB_PROTO = ""
if DEBUG:
    DOMAIN_NAME = "127.0.0.1:8000"
    WEB_PROTO = "http"
else:
    WEB_PROTO = "https"

# Addresses the Django app can be directly accessed from.
ALLOWED_HOSTS = ['raptorapp', '127.0.0.1']

# List of Super Users to create when no users are present. To be changed immediately after creation
ADMINS = (
    ('sradmin', 'sradmin@shadowraptor.net'),
)

# Application definition
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_bootstrap5',
    'ckeditor',
    'raptormc',
    'staffapps',
    'authprofiles',
    'gameservers'
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
    'gameservers.jobs.ServerWare',
    'authprofiles.userlist.ProfileManager'
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
DATABASES = {}

if USE_SQLITE:

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

else:

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

# Django Authentication
AUTHENTICATION_BACKENDS = [
    'authprofiles.auth.DiscordAuthBackend',
    'django.contrib.auth.backends.ModelBackend'
]

# Discord OAuth2 settings
DISCORD_AUTH_URL = ""
DISCORD_REDIRECT_URL = ""
DISCORD_APP_ID = getenv('DISCORD_APP_ID')
DISCORD_APP_SECRET = getenv('DISCORD_APP_SECRET')

if DEBUG:
    DISCORD_AUTH_URL = f"https://discord.com/api/oauth2/authorize?client_id={DISCORD_APP_ID}&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Foauth2%2Flogin%2Fredirect&response_type=code&scope=identify%20email"
    DISCORD_REDIRECT_URL = "http://127.0.0.1:8000/oauth2/login/redirect"
else:
    DISCORD_AUTH_URL = f"https://discord.com/api/oauth2/authorize?client_id={DISCORD_APP_ID}&redirect_uri=https%3A%2F%2F{DOMAIN_NAME}%2Foauth2%2Flogin%2Fredirect&response_type=code&scope=identify%20email"
    DISCORD_REDIRECT_URL = f"https://{DOMAIN_NAME}/oauth2/login/redirect"

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'debug': {
            'format': '[{levelname}] [{asctime}] {module} {process:d} {thread:d} {message}',
            'datefmt': '%H:%M:%S',
            'style': '{',
        },
        'simple_time': {
            'format': '[{levelname}] [{asctime}] {message}',
            'datefmt': '%H:%M',
            'style': '{',
        },
        'simple': {
            'format': '[{levelname}] {message}',
            'datefmt': '%H:%M',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple_time'
        },
        'log_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'debug',
            'filename': join(BASE_DIR, 'raptorWeb.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'log_file'],
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console', 'log_file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'raptormc.views': {
            'handlers': ['console', 'log_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'raptormc.jobs': {
            'handlers': ['console', 'log_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
         'raptormc.auth': {
            'handlers': ['console', 'log_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'staffapps.views': {
            'handlers': ['console', 'log_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'authprofiles.auth': {
            'handlers': ['console', 'log_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'authprofiles.views': {
            'handlers': ['console', 'log_file'],
            'level': 'DEBUG',
            'propagate': False,
        }
    }
}

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/New_York'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = join(join(BASE_DIR, '..'), join('config', 'static'))

# THIS MUST BE NAMED `STATICFILES_DIRS`
STATICFILES_DIRS = [
    STATIC_DIR,
]

# Media files (User submitted content)
MEDIA_URL = '/media/'
MEDIA_ROOT = MEDIA_DIR
DEFAULT_MEDIA = f'{WEB_PROTO}://{DOMAIN_NAME}/media/'

# Login URL
LOGIN_URL = 'raptormc/applications/login'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

BACKGROUND_TASK_RUN_ASYNC = True

# Enable/disable querying addresses provided in Server Models
ENABLE_SERVER_QUERY = True

# Base URL for Users in main app
BASE_USER_URL = 'user'

BOOTSTRAP5 = {

    # Set placeholder attributes to label if no placeholder is provided.
    'set_placeholder': False,

}

# Configure CKEditor, Rich Text Editor plugin
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'width': '120%',
    },
}
