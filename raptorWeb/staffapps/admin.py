from django.contrib import admin

from raptorWeb.staffapps.models import ModeratorApplication, AdminApplication

class AdminAppAdmin(admin.ModelAdmin):
    fields = (
        'age',
        'time',
        'mc_name',
        'discord_name',
        'voice_chat',
        'description',
        'modpacks',
        'experience',
        'why_join',
        'plugins',
        'api',
        'it_knowledge',
        'linux',
        'ptero'
    )
    
    readonly_fields = (
        'age',
        'time',
        'mc_name',
        'discord_name',
        'voice_chat',
        'description',
        'modpacks',
        'experience',
        'why_join',
        'plugins',
        'api',
        'it_knowledge',
        'linux',
        'ptero'
    )

class ModAppAdmin(admin.ModelAdmin):
    fields = (
        'age',
        'time',
        'mc_name',
        'discord_name',
        'voice_chat',
        'description',
        'modpacks',
        'experience',
        'why_join',
        'contact_uppers'
    )
    
    readonly_fields = (
        'age',
        'time',
        'mc_name',
        'discord_name',
        'voice_chat',
        'description',
        'modpacks',
        'experience',
        'why_join',
        'contact_uppers'
    )


admin.site.register(AdminApplication, AdminAppAdmin)
admin.site.register(ModeratorApplication, ModAppAdmin)
