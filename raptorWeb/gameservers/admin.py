from django.contrib import admin
from django.forms import TextInput, Textarea
from django.db import models

from raptorWeb.gameservers.models import Server, Player, ServerStatistic

class ServerAdmin(admin.ModelAdmin):
    """
    Object defining behavior and display of 
    RaptorUsers in the Django admin interface.
    """
    fieldsets: tuple[tuple[str, dict[str, tuple[str]]]] = (
        ('Server Information', {
            'fields': (
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
            'fields': ('server_state', 'player_count', 'announcement_count', 'in_maintenance', 'server_port')
        }),
        ('Discord Announcements', {
            'classes': ('collapse',),
            'fields': ('discord_announcement_channel_id', 'discord_modpack_role_id')
        })
    )

    readonly_fields: tuple[str] = (
        'server_state',
    )

    search_fields: list[str] = [
        'modpack_name',
    ]

    list_display: list[str] = ['modpack_name', 'modpack_version', 'in_maintenance']

admin.site.register(Server, ServerAdmin)
admin.site.register(Player)
admin.site.register(ServerStatistic)
