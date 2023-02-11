from django.apps import AppConfig


class AuthprofilesConfig(AppConfig):
    default_auto_field: str = 'django.db.models.BigAutoField'
    name: str = 'raptorWeb.authprofiles'
    verbose_name: str = 'User Profiles and Auth'
