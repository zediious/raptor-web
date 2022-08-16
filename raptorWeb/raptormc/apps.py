from django.apps import AppConfig
import os
import logging

class RaptormcConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'raptormc'

    def ready(self):
        from . import jobs

        if os.environ.get('RUN_MAIN', None) != 'true':

            pass
