from django.contrib import admin
from django.forms import TextInput, Textarea
from django.db import models
from raptormc.models import Server, InformativeText, PlayerCount, PlayerName, AdminApplication, ModeratorApplication, UserProfileInfo

class ServerAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'35'})},
        models.TextField: {'widget': Textarea(attrs={'rows':6, 'cols':60})},
    }

class InformativeTextAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'35'})},
        models.TextField: {'widget': Textarea(attrs={'rows':6, 'cols':60})},
    }

class AdminApplicationAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'35'})},
        models.TextField: {'widget': Textarea(attrs={'rows':6, 'cols':60})},
    }

class ModeratorApplicationAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'35'})},
        models.TextField: {'widget': Textarea(attrs={'rows':6, 'cols':60})},
    }

admin.site.register(Server, ServerAdmin)
admin.site.register(PlayerCount)
admin.site.register(PlayerName)
admin.site.register(InformativeText, InformativeTextAdmin)
admin.site.register(AdminApplication, AdminApplicationAdmin)
admin.site.register(ModeratorApplication, ModeratorApplicationAdmin)
admin.site.register(UserProfileInfo)
