from os.path import join, exists
from os import getenv, makedirs
from pathlib import Path
from dotenv import load_dotenv

from celery.schedules import crontab

from config.logging import LOGGING_DEFINITION

# Define project directories
BASE_DIR: str = Path(__file__).resolve().parent.parent
LOG_DIR: str = join(BASE_DIR, "logs")
RAPTORWEB_DIR: str = join(BASE_DIR, 'raptorWeb')
TEMPLATE_DIR: str = join(RAPTORWEB_DIR, "templates")
STATIC_DIR: str = join(RAPTORWEB_DIR, "static")
MEDIA_DIR: str = join(RAPTORWEB_DIR, "media")

RAPTORMC_TEMPLATE_DIR: str = join(TEMPLATE_DIR, "raptormc")
PANEL_TEMPLATE_DIR: str = join(TEMPLATE_DIR, "panel")
RAPTORBOT_TEMPLATE_DIR: str = join(TEMPLATE_DIR, 'raptorbot')
GAMESERVERS_TEMPLATE_DIR: str = join(TEMPLATE_DIR, 'gameservers')
DONATIONS_TEMPLATE_DIR: str = join(TEMPLATE_DIR, 'donations')
STAFFAPPS_TEMPLATE_DIR: str = join(TEMPLATE_DIR, 'staffapps')
AUTH_TEMPLATE_DIR: str = join(TEMPLATE_DIR, 'authprofiles')

# Load .env file
load_dotenv(join(BASE_DIR, 'stack.env'))

# Django secret key from .env
SECRET_KEY: str = getenv('DJANGO_SECRET_KEY')

# SECURITY WARNING: Neither of the below two True in production!
DEBUG: bool = True if getenv('DEBUG') == "True" else False
USE_SQLITE: bool = True if getenv('USE_SQLITE') == "True" else False

# Set RUNNING_IN_DOCKER to True if you are running this in a Docker container
RUNNING_IN_DOCKER: bool = True if getenv('RUNNING_IN_DOCKER') == "True" else False

# Configure "DOMAIN_NAME" to match the domain name you will use (no www)
DOMAIN_NAME: str = getenv('DOMAIN_NAME')

# Configure web protocol based on DEBUG status
WEB_PROTO: str = ""
if DEBUG and RUNNING_IN_DOCKER:
    DOMAIN_NAME: str = "localhost"
    WEB_PROTO: str = "https"
if DEBUG and not RUNNING_IN_DOCKER:
    DOMAIN_NAME: str = "127.0.0.1:8000"
    WEB_PROTO: str = "http"
else:
    WEB_PROTO: str = "https"

# Addresses the Django app can be directly accessed from.
ALLOWED_HOSTS: list[str] = ['raptorapp', '127.0.0.1', 'localhost']

# Superuser to create when no users are present. To be changed immediately after creation
ADMINS: list[tuple[str]] = [(
    (getenv('DEFAULT_SUPERUSER_USERNAME'), getenv('DEFAULT_SUPERUSER_EMAIL')),
    ('error_logger_user', getenv('ERROR_LOG_EMAIL')),
)]

# CSRF
SESSION_COOKIE_SECURE: bool = True
CSRF_COOKIE_SECURE: bool = True
CSRF_TRUSTED_ORIGINS: list[str] = [f'{WEB_PROTO}://{DOMAIN_NAME}',
                                   f'{WEB_PROTO}://www.{DOMAIN_NAME}']

# Application/Middleware definitions
INSTALLED_APPS: list[str] = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_bootstrap5',
    'tinymce',
    'captcha',
    'raptorWeb.raptormc',
    'raptorWeb.staffapps',
    'raptorWeb.authprofiles',
    'raptorWeb.gameservers',
    'raptorWeb.donations',
    'raptorWeb.raptorbot',
    'raptorWeb.panel',
    'paypal.standard.ipn'
]

MIDDLEWARE: list[str] = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'raptorWeb.raptorbot.botware.RaptorBotWare',
    'raptorWeb.panel.middleware.PanelMessages',
    'raptorWeb.raptormc.hx_reroute_middleware.HxReroute'
]

ROOT_URLCONF: str = 'config.urls'

TEMPLATES: list[dict] = [
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
                'raptorWeb.panel.context_processor.context_process',
                'raptorWeb.authprofiles.context_processor.all_users_to_context',
                'raptorWeb.raptorbot.context_processor.add_discord_guild_data',
                'raptorWeb.gameservers.context_processor.server_settings_to_context',
            ],
        },
    },
]

WSGI_APPLICATION: str = 'config.wsgi.application'
ASGI_APPLICATION: str = 'config.asgi.application'

# Email
USE_CONSOLE_EMAIL: bool = True if getenv('USE_CONSOLE_EMAIL') == "True" else False
SERVER_EMAIL: str = str(getenv('EMAIL_HOST_USER'))
EMAIL_BACKEND: str = 'django.core.mail.backends.smtp.EmailBackend'
if USE_CONSOLE_EMAIL:
    EMAIL_BACKEND: str = 'django.core.mail.backends.filebased.EmailBackend'
    EMAIL_FILE_PATH = f"{LOG_DIR}/email" 

EMAIL_USE_TLS: bool = True
EMAIL_HOST: str = str(getenv('EMAIL_HOST')) if str(getenv('EMAIL_HOST')) != '' else 'test@example.com'
EMAIL_PORT: int = int(getenv('EMAIL_PORT')) if getenv('EMAIL_PORT') != '' else 587
EMAIL_HOST_USER: str = str(getenv('EMAIL_HOST_USER')) if str(getenv('EMAIL_HOST_USER')) != '' else 'Test'
EMAIL_HOST_PASSWORD: str = str(getenv('EMAIL_HOST_PASSWORD')) if str(getenv('EMAIL_HOST_PASSWORD')) != '' else ''

# Database
DATABASES: dict = {}

if USE_SQLITE:

    DATABASES: dict = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

else:

    DATABASES: dict = {
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
AUTH_PASSWORD_VALIDATORS: list[dict] = [
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
PASSWORD_HASHERS: list[str] = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

# Django Authentication
AUTHENTICATION_BACKENDS: list[str] = [
    'raptorWeb.authprofiles.auth.DiscordAuthBackend',
    'django.contrib.auth.backends.ModelBackend'
]

# Logging configuration

# Create log directory if it does not exist
if not exists(LOG_DIR):
    makedirs(LOG_DIR)

LOGGING: dict = LOGGING_DEFINITION

# Internationalization
LANGUAGE_CODE: str = getenv('LANGUAGE_CODE')
TIME_ZONE: str = getenv('TIME_ZONE')
USE_I18N: bool = True
USE_L10N: bool = True
USE_TZ: bool = True

# Static files (CSS, JavaScript, Images)
STATIC_URL: str = '/static/'
STATIC_ROOT: str = join(join(BASE_DIR, 'docker'), join('static'))

# THIS MUST BE NAMED `STATICFILES_DIRS`
STATICFILES_DIRS: list[str] = [
    STATIC_DIR,
]

# Media files (User submitted content)
MEDIA_URL: str = '/media/'
MEDIA_ROOT: str = MEDIA_DIR
DEFAULT_MEDIA: str = f'{WEB_PROTO}://{DOMAIN_NAME}/media/'

# Default primary key field type
DEFAULT_AUTO_FIELD: str = 'django.db.models.BigAutoField'

BACKGROUND_TASK_RUN_ASYNC: bool = True

# ** Settings for "donations" app **
STRIPE_PUBLISHABLE_KEY =  '' if str(getenv('STRIPE_PUBLISHABLE_KEY')) == '' else  str(getenv('STRIPE_PUBLISHABLE_KEY'))
STRIPE_SECRET_KEY = '' if str(getenv('STRIPE_SECRET_KEY')) == '' else str(getenv('STRIPE_SECRET_KEY'))
STRIPE_WEBHOOK_SECRET = '' if str(getenv('STRIPE_WEBHOOK_SECRET')) == '' else str(getenv('STRIPE_WEBHOOK_SECRET'))
PAYPAL_RECEIVER_EMAIL = '' if getenv('PAYPAL_RECEIVER_EMAIL') == '' else getenv('PAYPAL_RECEIVER_EMAIL')
PAYPAL_DEV_WEBHOOK_DOMAIN = '' if getenv('PAYPAL_DEV_WEBHOOK_DOMAIN') == '' else getenv('PAYPAL_DEV_WEBHOOK_DOMAIN')
PAYPAL_TEST = True if DEBUG else False

# Path to json file to import servers from
IMPORT_JSON_LOCATION: str = join(BASE_DIR, 'server_data_full.json')

# ** Settings for "authprofiles" app **
AUTH_USER_MODEL: str = 'authprofiles.RaptorUser'
LOGIN_URL: str = '/login/'
BASE_USER_URL: str = 'user'
USER_RESET_URL: str = 'reset'
DISCORD_APP_ID: str = getenv('DISCORD_OAUTH_APP_ID')
DISCORD_APP_SECRET: str = getenv('DISCORD_OAUTH_APP_SECRET')
DISCORD_REDIRECT_URL: str = f"{WEB_PROTO}://{DOMAIN_NAME}/api/user/oauth2/login/redirect"
DISCORD_AUTH_URL: str = ("https://discord.com/api/oauth2/authorize?"
                        f"client_id={DISCORD_APP_ID}"
                        f"&redirect_uri={DISCORD_REDIRECT_URL}&response_type=code&scope=identify%20email")

# ** Settings for "raptorbot" app **
DISCORD_BOT_TOKEN: str = getenv('DISCORD_BOT_TOKEN')
DISCORD_BOT_DESCRIPTION: str = getenv('DISCORD_BOT_DESCRIPTION')
RUN_BOT: bool = True if getenv('RUN_BOT') == 'True' else False

# ** Celery Settings **
CELERY_BEAT_SCHEDULE = {
    'donation_command_rerun': {
        'task': 'raptorWeb.donations.tasks.resend_server_commands',
        'schedule': crontab(minute='*/5'),
    },
    'donation_role_readd': {
        'task': 'raptorWeb.donations.tasks.readd_discord_bot_roles',
        'schedule': crontab(minute='*/5'),
    },
    'clear_donation_goal': {
        'task': 'raptorWeb.donations.tasks.clear_donation_goal',
        'schedule': crontab(day_of_month='1'),
    },
    'check_for_deletable_users': {
        'task': 'raptorWeb.authprofiles.tasks.check_for_deletable_users',
        'schedule': crontab(minute='*/15'),
    },
    'check_for_deletable_qr_images': {
        'task': 'raptorWeb.authprofiles.tasks.check_for_deletable_qr_images',
        'schedule': crontab(minute='*/5'),
    }
}

# ** Settings for "django_bootstrap5" app **
BOOTSTRAP5: dict = {

    # Set placeholder attributes to label if no placeholder is provided.
    'set_placeholder': False,

}

# ** Settings for "django-tinymce" app **
TINYMCE_DEFAULT_CONFIG: dict = {
        "theme": "silver",
        "height": 500,
        "menubar": True,
        "plugins": "advlist,autolink,lists,link,image,charmap,print,preview,anchor,"
        "searchreplace,visualblocks,code,fullscreen,insertdatetime,media,table,paste,"
        "code,help,wordcount",
        "toolbar": "undo redo | formatselect | "
        "bold italic forecolor backcolor | alignleft aligncenter "
        "alignright alignjustify | bullist numlist outdent indent | "
        "removeformat | help",
    }

