from django.contrib import admin

from raptorWeb.gameservers.models import Server, Player, ServerStatistic

class ServerAdmin(admin.ModelAdmin):
    """
    Object defining behavior and display of 
    Servers in the Django admin interface.
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

class PlayerAdmin(admin.ModelAdmin):
    """
    Object defining behavior and display of 
    Players in the Django admin interface.
    """
    fieldsets: tuple[tuple[str, dict[str, tuple[str]]]] = (
        ('Player Information', {
            'fields': (
                'server',
                'name')
        }),
    )

    readonly_fields: tuple[str] = (
        'server',
        'name'
    )

    search_fields: list[str] = [
        'name',
    ]

    list_display: list[str] = ['name', 'server']

class ServerStatisticAdmin(admin.ModelAdmin):
    """
    Object defining behavior and display of 
    ServerStatistics in the Django admin interface.
    """
    fieldsets: tuple[tuple[str, dict[str, tuple[str]]]] = (
        ('Global Server Statistics', {
            'fields': (
                'total_player_count',)
        }),
    )

    readonly_fields: tuple[str] = (
        'total_player_count',
    )

    list_display: list[str] = ['total_player_count']

admin.site.register(Server, ServerAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(ServerStatistic, ServerStatisticAdmin)
