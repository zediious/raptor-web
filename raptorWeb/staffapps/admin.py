from django.contrib import admin

from raptorWeb.staffapps.models import ModeratorApplication, AdminApplication


class AdminAppAdmin(admin.ModelAdmin):
    fields = (
        'approved',
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

    list_display: list[str] = ['discord_name', 'approved']

    def has_add_permission(self, request, obj=None):
        return False


class ModAppAdmin(admin.ModelAdmin):
    fields = (
        'approved',
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

    list_display: list[str] = ['discord_name', 'approved']

    def has_add_permission(self, request, obj=None):
        return False


admin.site.register(AdminApplication, AdminAppAdmin)
admin.site.register(ModeratorApplication, ModAppAdmin)
