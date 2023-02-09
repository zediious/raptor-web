from os.path import join
from os import getenv
from pathlib import Path
from dotenv import load_dotenv

# Define project directories
BASE_DIR = Path(__file__).resolve().parent.parent
RAPTORWEB_DIR = join(BASE_DIR, 'raptorWeb')
TEMPLATE_DIR = join(RAPTORWEB_DIR, "templates")
STATIC_DIR = join(RAPTORWEB_DIR, "static")
MEDIA_DIR = join(RAPTORWEB_DIR, "media")

RAPTORMC_TEMPLATE_DIR = join(TEMPLATE_DIR, "raptormc")
GAMESERVERS_TEMPLATE_DIR = join(TEMPLATE_DIR, 'gameservers')
STAFFAPPS_TEMPLATE_DIR = join(TEMPLATE_DIR, 'staffapps')
AUTH_TEMPLATE_DIR = join(TEMPLATE_DIR, 'authprofiles')

# Load .env file
load_dotenv()

# Django secret key from .env
SECRET_KEY = getenv('DJANGO_SECRET_KEY')

# SECURITY WARNING: Neither of the below two True in production!
DEBUG = True if getenv('DEBUG') == "True" else False
USE_SQLITE = True if getenv('USE_SQLITE') == "True" else False

# Set RUNNING_IN_DOCKER to True if you are running this in a Docker container
RUNNING_IN_DOCKER = True if getenv('RUNNING_IN_DOCKER') == "True" else False

# Configure "DOMAIN_NAME" to match the domain name you will use (no www)
DOMAIN_NAME = getenv('DOMAIN_NAME'),

# Configure web protocol based on DEBUG status
WEB_PROTO = ""
if DEBUG and RUNNING_IN_DOCKER:
    DOMAIN_NAME = "localhost"
    WEB_PROTO = "https"
if DEBUG and not RUNNING_IN_DOCKER:
    DOMAIN_NAME = "127.0.0.1:8000"
    WEB_PROTO = "http"
else:
    WEB_PROTO = "https"

# Addresses the Django app can be directly accessed from.
ALLOWED_HOSTS = ['raptorapp', '127.0.0.1', 'localhost']

# List of Super Users to create when no users are present. To be changed immediately after creation
ADMINS = (
    ('sradmin', 'sradmin@shadowraptor.net'),
)

# CSRF
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_TRUSTED_ORIGINS = [f'{WEB_PROTO}://{DOMAIN_NAME}']

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
    'captcha',
    'raptorWeb.raptormc',
    'raptorWeb.staffapps',
    'raptorWeb.authprofiles',
    'raptorWeb.gameservers',
    'raptorWeb.raptorbot'
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
    'raptorWeb.gameservers.jobs.ServerWare',
    'raptorWeb.raptorbot.botware.RaptorBotWare'
]

ROOT_URLCONF = 'config.urls'

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
                'raptorWeb.raptormc.context_processor.context_process',
                'raptorWeb.authprofiles.context_processor.all_users_to_context',
                'raptorWeb.raptorbot.context_processor.add_discord_guild_data',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

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
    'raptorWeb.authprofiles.auth.DiscordAuthBackend',
    'django.contrib.auth.backends.ModelBackend'
]

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
        'bot_log_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'debug',
            'filename': join(BASE_DIR, 'raptorBot.log'),
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
        },
        'raptorbot.botware': {
            'handlers': ['console', 'bot_log_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'discordbot.bot': {
            'handlers': ['console', 'bot_log_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'discordbot.util': {
            'handlers': ['console', 'bot_log_file'],
            'level': 'DEBUG',
            'propagate': False,
        }
    }
}

# Internationalization
LANGUAGE_CODE = getenv('LANGUAGE_CODE')
TIME_ZONE = getenv('TIME_ZONE')
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

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

BACKGROUND_TASK_RUN_ASYNC = True

# ** Settings for "gameservers" app **
# Set to True to query addresses of Servers
ENABLE_SERVER_QUERY = True if getenv('ENABLE_SERVER_QUERY') == "True" else False
# Set to True to import a server_data_full.json on start
IMPORT_SERVERS = True if getenv('IMPORT_SERVERS') == "True" else False
# Set to True to delete existing servers when performing an import
DELETE_EXISTING = True if getenv('DELETE_EXISTING') == "True" else False
# Location of json file to import servers from
IMPORT_JSON_LOCATION = join(BASE_DIR, 'server_data_full.json')
# Location of LOCk file used to time gameserver queries
LOCK_FILE_PATH = join(BASE_DIR, 'playerCounts.LOCK')

# ** Settings for "authprofiles" app **
AUTH_USER_MODEL = 'authprofiles.RaptorUser'
LOGIN_URL = '/login/'
BASE_USER_URL = 'user'

DISCORD_APP_ID = getenv('DISCORD_OAUTH_APP_ID')
DISCORD_APP_SECRET = getenv('DISCORD_OAUTH_APP_SECRET')
DISCORD_AUTH_URL = f"https://discord.com/api/oauth2/authorize?client_id={DISCORD_APP_ID}&redirect_uri={WEB_PROTO}%3A%2F%2F{DOMAIN_NAME}%2Foauth2%2Flogin%2Fredirect&response_type=code&scope=identify%20email"
DISCORD_REDIRECT_URL = f"{WEB_PROTO}://{DOMAIN_NAME}/oauth2/login/redirect"

IMPORT_USERS = True if getenv('IMPORT_USERS') == 'True' else False

# ** Settings for "raptorbot" app **
# Set to True to enable website using scraped Global Announcements
USE_GLOBAL_ANNOUNCEMENT = True if getenv('USE_GLOBAL_ANNOUNCEMENT') == "True" else False
# Set to True to enable Raptor Bot scraping Discord announcements for each server
SCRAPE_SERVER_ANNOUNCEMENT = True if getenv('SCRAPE_SERVER_ANNOUNCEMENT') == "True" else False
# Settings for the Discord Bot
DISCORD_BOT_TOKEN = getenv('DISCORD_BOT_TOKEN')
DISCORD_BOT_DESCRIPTION = getenv('DISCORD_BOT_DESCRIPTION')
DISCORD_GUILD = int(getenv('DISCORD_GUILD'))
GLOBAL_ANNOUNCEMENT_CHANNEL_ID = int(getenv('GLOBAL_ANNOUNCEMENT_CHANNEL_ID'))
STAFF_ROLE_ID = int(getenv('STAFF_ROLE_ID'))

# ** Settings for "django_bootstrap5" app **
BOOTSTRAP5 = {

    # Set placeholder attributes to label if no placeholder is provided.
    'set_placeholder': False,

}

# ** Settings for "CKEditor-django" app **
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'width': '120%',
    },
}
