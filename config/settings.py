from os.path import join
from os import getenv
from pathlib import Path
from dotenv import load_dotenv

# Define project directories
BASE_DIR: str = Path(__file__).resolve().parent.parent
RAPTORWEB_DIR: str = join(BASE_DIR, 'raptorWeb')
TEMPLATE_DIR: str = join(RAPTORWEB_DIR, "templates")
STATIC_DIR: str = join(RAPTORWEB_DIR, "static")
MEDIA_DIR: str = join(RAPTORWEB_DIR, "media")

RAPTORMC_TEMPLATE_DIR: str = join(TEMPLATE_DIR, "raptormc")
GAMESERVERS_TEMPLATE_DIR: str = join(TEMPLATE_DIR, 'gameservers')
STAFFAPPS_TEMPLATE_DIR: str = join(TEMPLATE_DIR, 'staffapps')
AUTH_TEMPLATE_DIR: str = join(TEMPLATE_DIR, 'authprofiles')

# Load .env file
load_dotenv()

# Django secret key from .env
SECRET_KEY: str = getenv('DJANGO_SECRET_KEY')

# SECURITY WARNING: Neither of the below two True in production!
DEBUG: bool = True if getenv('DEBUG') == "True" else False
USE_SQLITE: bool = True if getenv('USE_SQLITE') == "True" else False

# Set RUNNING_IN_DOCKER to True if you are running this in a Docker container
RUNNING_IN_DOCKER: bool = True if getenv('RUNNING_IN_DOCKER') == "True" else False

# Configure "DOMAIN_NAME" to match the domain name you will use (no www)
DOMAIN_NAME: str = getenv('DOMAIN_NAME'),

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
ADMINS: tuple[str] = (
    (getenv('DEFAULT_SUPERUSER_USERNAME'), getenv('DEFAULT_SUPERUSER_EMAIL')),
)

# CSRF
SESSION_COOKIE_SECURE: bool = True
CSRF_COOKIE_SECURE: bool = True
CSRF_TRUSTED_ORIGINS: list[str] = [f'{WEB_PROTO}://{DOMAIN_NAME}']

# Application/Middleware definitions
INSTALLED_APPS: list[str] = [
    'jazzmin',
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
    'raptorWeb.raptorbot'
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
    'raptorWeb.gameservers.jobs.ServerWare',
    'raptorWeb.raptorbot.botware.RaptorBotWare'
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
EMAIL_BACKEND: str = 'django.core.mail.backends.smtp.EmailBackend'
if USE_CONSOLE_EMAIL:
    EMAIL_BACKEND: str = 'django.core.mail.backends.console.EmailBackend'

EMAIL_USE_TLS: bool = True
EMAIL_HOST: str = str(getenv('EMAIL_HOST'))
EMAIL_PORT: int = int(getenv('EMAIL_PORT'))
EMAIL_HOST_USER: str = str(getenv('EMAIL_HOST_USER'))
EMAIL_HOST_PASSWORD: str = str(getenv('EMAIL_HOST_PASSWORD'))

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
LOGGING: dict = {
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
        'authprofiles.models': {
            'handlers': ['console', 'log_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'gameservers.views': {
            'handlers': ['console', 'log_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'gameservers.models': {
            'handlers': ['console', 'log_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'raptorbot.botware': {
            'handlers': ['console', 'bot_log_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'raptorbot.discordbot.bot': {
            'handlers': ['console', 'bot_log_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'raptorbot.discordbot.util': {
            'handlers': ['console', 'bot_log_file'],
            'level': 'DEBUG',
            'propagate': False,
        }
    }
}

# Internationalization
LANGUAGE_CODE: str = getenv('LANGUAGE_CODE')
TIME_ZONE: str = getenv('TIME_ZONE')
USE_I18N: bool = True
USE_L10N: bool = True
USE_TZ: bool = True

# Static files (CSS, JavaScript, Images)
STATIC_URL: str = '/static/'
STATIC_ROOT: str = join(join(BASE_DIR, '..'), join('config', 'static'))

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

# ** Settings for "raptormc" app **
ADMIN_BRAND_NAME = "Default" if getenv('ADMIN_BRAND_NAME') == '' else getenv('ADMIN_BRAND_NAME')

# ** Settings for "gameservers" app **
ENABLE_SERVER_QUERY: bool = True if getenv('ENABLE_SERVER_QUERY') == "True" else False
SERVER_PAGINATION_COUNT: int = int(getenv('SERVER_PAGINATION_COUNT'))
IMPORT_SERVERS: bool = True if getenv('IMPORT_SERVERS') == "True" else False
DELETE_EXISTING: bool = True if getenv('DELETE_EXISTING') == "True" else False
# Path to json file to import servers from
IMPORT_JSON_LOCATION: str = join(BASE_DIR, 'server_data_full.json')

# ** Settings for "authprofiles" app **
AUTH_USER_MODEL: str = 'authprofiles.RaptorUser'
LOGIN_URL: str = '/login/'
BASE_USER_URL: str = getenv('BASE_USER_URL')
USER_RESET_URL: str = getenv('USER_RESET_URL')
DISCORD_APP_ID: str = getenv('DISCORD_OAUTH_APP_ID')
DISCORD_APP_SECRET: str = getenv('DISCORD_OAUTH_APP_SECRET')
DISCORD_REDIRECT_URL: str = f"{WEB_PROTO}://{DOMAIN_NAME}/api/user/oauth2/login/redirect"
DISCORD_AUTH_URL: str = ("https://discord.com/api/oauth2/authorize?"
                        f"client_id={DISCORD_APP_ID}"
                        f"&redirect_uri={DISCORD_REDIRECT_URL}&response_type=code&scope=identify%20email")
IMPORT_USERS: bool = True if getenv('IMPORT_USERS') == 'True' else False

# ** Settings for "raptorbot" app **
USE_GLOBAL_ANNOUNCEMENT: bool = True if getenv('USE_GLOBAL_ANNOUNCEMENT') == "True" else False
SCRAPE_SERVER_ANNOUNCEMENT: bool = True if getenv('SCRAPE_SERVER_ANNOUNCEMENT') == "True" else False
DISCORD_BOT_TOKEN: str = getenv('DISCORD_BOT_TOKEN')
DISCORD_BOT_DESCRIPTION: str = getenv('DISCORD_BOT_DESCRIPTION')
DISCORD_GUILD: int = int(getenv('DISCORD_GUILD'))
GLOBAL_ANNOUNCEMENT_CHANNEL_ID: int = int(getenv('GLOBAL_ANNOUNCEMENT_CHANNEL_ID'))
STAFF_ROLE_ID: int = int(getenv('STAFF_ROLE_ID'))

# ** Settings for "django-jazzmin" app **
JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": f"{ADMIN_BRAND_NAME} Admin",

    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": f"{ADMIN_BRAND_NAME}",

    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": f"{ADMIN_BRAND_NAME}",

    # Logo to use for your site, must be present in static files, used for brand on top left
    "site_logo": "image/ShadowRaptorAvatar.webp",

    # Logo to use for your site, must be present in static files, used for login form logo (defaults to site_logo)
    "login_logo": "image/ShadowRaptorAvatar.webp",

    # Logo to use for login form in dark themes (defaults to login_logo)
    "login_logo_dark": None,

    # CSS classes that are applied to the logo above
    "site_logo_classes": "img-circle",

    # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
    "site_icon": None,

    # Welcome text on the login screen
    "welcome_sign": f"Welcome to {ADMIN_BRAND_NAME}",

    # Copyright on the footer
    "copyright": "Admin theme by Acme Library Ltd",

    # List of model admins to search from the search bar, search bar omitted if excluded
    # If you want to use a single search field you dont need to use a list, you can use a simple string 
    "search_model": ["authprofiles.RaptorUser", "gameservers.Server"],

    # Field name on user model that contains avatar ImageField/URLField/Charfield or a callable that receives the user
    "user_avatar": 'user_profile_info.profile_picture',

    # Links to put along the top menu
    "topmenu_links": [

        {"name": "Return to Site", "url": "/", "new_window": False},
        {"name": "Control Panel", "url": "/panel", "new_window": False},

        {"app": "raptormc"},
        {"app": "gameservers"},
        {"app": "raptorbot"},
        {"app": "staffapps"},
        {"app": "authprofiles"},
    ],

    # Additional links to include in the user menu on the top right ("app" url type is not allowed)
    "usermenu_links": [
        {"model": "auth.user"}
    ],

    # Sidebar
    "show_sidebar": True,
    "navigation_expanded": False,

    # Hide these apps when generating side menu e.g (auth)
    "hide_apps": [],

    # Hide these models when generating side menu (e.g auth.user)
    "hide_models": [],

    # List of apps (and/or models) to base side menu ordering off of (does not need to contain all apps/models)
    "order_with_respect_to": ["raptormc", "gameservers", "raptorbot", "staffapps", "authprofiles"],

    # Custom links to append to app groups, keyed on app name
    "custom_links": {
        "raptorbot": [{
            "name": "Bot Actions", 
            "url": "../../../panel", 
            "icon": "fas fa-joystick",
            "permissions": ["raptorbot.view_discordguild"]
        }]
    },

    # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free&v=5.0.0,5.0.1,5.0.10,5.0.11,5.0.12,5.0.13,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.13.0,5.12.0,5.11.2,5.11.1,5.10.0,5.9.0,5.8.2,5.8.1,5.7.2,5.7.1,5.7.0,5.6.3,5.5.0,5.4.2
    # for the full list of 5.13.0 free icon classes
    "icons": {
        "raptormc": "fas fa-book",
        "raptormc.InformativeText": "fas fa-scroll",
        "raptormc.NavbarLink": "fas fa-map-marker",
        "raptormc.NavbarDropdown": "fas fa-map-marker-plus",
        "raptormc.SiteInformation": "fas fa-clipboard-list",
    },
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    # Use modals instead of popups
    "related_modal_active": True,

    # Relative paths to custom CSS/JS scripts (must be present in static files)
    "custom_css": None,
    "custom_js": None,

    # Whether to link font from fonts.googleapis.com (use custom_css to supply font otherwise)
    "use_google_fonts_cdn": True,

    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": False,

}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": True,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": False,
    "accent": "accent-lightblue",
    "navbar": "navbar-gray-dark navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-info",
    "sidebar_nav_small_text": True,
    "sidebar_disable_expand": True,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "cyborg",
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-outline-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-outline-success"
    },
    "actions_sticky_top": False
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

