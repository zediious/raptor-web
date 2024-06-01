from os.path import join
from pathlib import Path

LOG_DIR: str = join(Path(__file__).resolve().parent.parent, "logs")

LOGGING_DEFINITION = {
    'version': 1,
    'disable_existing_loggers': False,
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
    },
    'formatters': {
        'debug': {
            'format': '[{levelname}] [{asctime}] {module} {process:d} {thread:d} {message}',
            'datefmt': '%Y:%m:%d-%H:%M:%S',
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
            'class': 'logging.StreamHandler',
            'formatter': 'debug'
        },
        'django_log_file': {
            'class': 'logging.FileHandler',
            'formatter': 'debug',
            'filename': join(LOG_DIR, 'django.log'),
        },
        'celery_log_file': {
            'class': 'logging.FileHandler',
            'formatter': 'debug',
            'filename': join(LOG_DIR, 'celery.log'),
        },
        'log_file': {
            'class': 'logging.FileHandler',
            'formatter': 'debug',
            'filename': join(LOG_DIR, 'raptorWeb.log'),
        },
        'bot_log_file': {
            'class': 'logging.FileHandler',
            'formatter': 'debug',
            'filename': join(LOG_DIR, 'raptorBot.log'),
        },
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'django_log_file', 'mail_admins'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console', 'django_log_file', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'config.celery': {
            'handlers': ['console', 'celery_log_file', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'raptormc.views': {
            'handlers': ['console', 'log_file', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'raptormc.models': {
            'handlers': ['console', 'log_file', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'raptormc.urlStrip': {
            'handlers': ['console', 'log_file', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'raptormc.addParams': {
            'handlers': ['console', 'log_file', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'raptormc.routes': {
            'handlers': ['console', 'log_file', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'panel.routes': {
            'handlers': ['console', 'log_file', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'panel.models': {
            'handlers': ['console', 'log_file', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'panel.views': {
            'handlers': ['console', 'log_file', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'staffapps.views': {
            'handlers': ['console', 'log_file', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'authprofiles.auth': {
            'handlers': ['console', 'log_file', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'authprofiles.views': {
            'handlers': ['console', 'log_file', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'authprofiles.models': {
            'handlers': ['console', 'log_file', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'authprofiles.authTags': {
            'handlers': ['console', 'log_file', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'authprofiles.tokens': {
            'handlers': ['console', 'log_file', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'authprofiles.tasks': {
            'handlers': ['console', 'log_file', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'gameservers.views': {
            'handlers': ['console', 'log_file', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'gameservers.models': {
            'handlers': ['console', 'log_file', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'gameservers.serverTags': {
            'handlers': ['console', 'log_file', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'donations.models': {
            'handlers': ['console', 'log_file', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'donations.views': {
            'handlers': ['console', 'log_file', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'donations.payments.stripe': {
            'handlers': ['console', 'log_file', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'donations.payments.paypal': {
            'handlers': ['console', 'log_file', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'donations.donationTags': {
            'handlers': ['console', 'log_file', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'donations.tasks': {
            'handlers': ['console', 'celery_log_file', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'raptorbot.models': {
            'handlers': ['console', 'bot_log_file', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'raptorbot.botware': {
            'handlers': ['console', 'bot_log_file', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'raptorbot.discordbot.bot': {
            'handlers': ['console', 'bot_log_file', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'raptorbot.discordbot.util.presence': {
            'handlers': ['console', 'bot_log_file', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'raptorbot.discordbot.util.announcements': {
            'handlers': ['console', 'bot_log_file', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'raptorbot.discordbot.util.embed': {
            'handlers': ['console', 'bot_log_file', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'raptorbot.discordbot.util.messages': {
            'handlers': ['console', 'bot_log_file'],
            'handlers': ['console', 'bot_log_file', 'mail_admins'],
            'propagate': False,
        },
        'raptorbot.discordbot.util.task_check': {
            'handlers': ['console', 'bot_log_file', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': False,
        }
    }
}