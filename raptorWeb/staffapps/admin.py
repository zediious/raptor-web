from django.contrib import admin

from staffapps.models import ModeratorApplication, AdminApplication

admin.site.register(AdminApplication)
admin.site.register(ModeratorApplication)
