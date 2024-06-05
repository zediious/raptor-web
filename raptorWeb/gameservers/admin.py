from django.contrib import admin
from django.forms import ModelForm

from tinymce.widgets import TinyMCE

from raptorWeb.gameservers.models import Server, Player

class ServerAdminForm(ModelForm):
    class Meta:
        model = Server
        widgets = {
            'modpack_description': TinyMCE,
            'server_description': TinyMCE,
            'server_rules': TinyMCE,
            'server_banned_items': TinyMCE,
            'server_vote_links': TinyMCE
        }
        fields = '__all__'

class ServerAdmin(admin.ModelAdmin):
    """
    Object defining behavior and display of 
    Servers in the Django admin interface.
    """
    form = ServerAdminForm

    fieldsets: tuple[tuple[str, dict[str, tuple[str]]]] = (
        ('Server Information', {
            'fields': (
                'archived',
                'modpack_picture',
                'modpack_url',
                'modpack_name',
                'modpack_version',
                'server_address',
                'modpack_description',
                'server_description',
                'server_rules',
                'server_banned_items',
                'server_vote_links')
        }),
        ('Server Querying', {
            'classes': ('collapse',),
            'fields': ('in_maintenance', 'server_port', 'server_state', 'player_count', 'announcement_count')
        }),
        ('Discord Announcements', {
            'classes': ('collapse',),
            'fields': ('discord_announcement_channel_id', 'discord_modpack_role_id')
        }),
        ('Donations', {
            'classes': ('collapse',),
            'fields': ('rcon_address', 'rcon_port', 'rcon_password')
        })
    )

    readonly_fields: tuple[str] = (
        'server_state',
        'announcement_count',
        'player_count'
    )

    search_fields: list[str] = [
        'modpack_name',
    ]

    list_display: list[str] = ['modpack_name', 'modpack_version', 'in_maintenance', 'archived']

class PlayerAdmin(admin.ModelAdmin):
    """
    Object defining behavior and display of 
    Players in the Django admin interface.
    """
    fieldsets: tuple[tuple[str, dict[str, tuple[str]]]] = (
        ('Player Information', {
            'fields': (
                'server',
                'name',
                'online',
                'last_online',
                'first_joined')
        }),
    )

    readonly_fields: tuple[str] = (
        'server',
        'name',
        'online',
        'last_online'
    )

    search_fields: list[str] = [
        'name',
    ]

    list_display: list[str] = ['name', 'server', 'online', 'last_online']

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

admin.site.register(Server, ServerAdmin)
admin.site.register(Player, PlayerAdmin)
