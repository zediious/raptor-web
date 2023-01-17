from django.apps import AppConfig
import os
import logging

class RaptormcConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'raptormc'
    verbose_name = 'ShadowRaptorMC Website'

    def ready(self):

        if os.environ.get('RUN_MAIN', None) != 'true':

            pass
