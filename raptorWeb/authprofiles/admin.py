from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin

from raptorWeb.authprofiles.models import RaptorUser, UserProfileInfo, DiscordUserInfo, DeletionQueueForUser


class RaptorUserAdmin(UserAdmin):
    """
    Object defining behavior and display of 
    RaptorUsers in the Django admin interface.
    """
    fieldsets: tuple[tuple[str, dict[str, tuple[str]]]] = (
        ('General', {
            'fields': (
                'user_profile_info',
                'discord_user_info',
                'is_active',
                'date_queued_for_delete',
                'is_discord_user',
                'email',
                'first_name',
                'last_name',
                'username',
                'user_slug',
                'date_joined',
                'last_login',
                'toasts_seen')
        }),
        ('Permissions', {
            'classes': ('collapse',),
            'fields': ('user_permissions','groups')
        }),
        ('Sensitive', {
            'classes': ('collapse',),
            'fields': ('is_superuser', 'is_staff', 'password', 'password_reset_token')
        })
    )

    readonly_fields: tuple[str] = (
        'is_discord_user',
        'date_joined',
        'last_login',
        'user_profile_info',
        'discord_user_info'
    )

    search_fields: list[str] = [
        'username',
        'user_slug',
        'email',
        'discord_user_info__tag'
    ]

    list_display: list[str] = ['username', 'email', 'is_discord_user', 'is_staff', 'is_active', 'date_joined']


class UserProfileInfoAdmin(admin.ModelAdmin):
    """
    Object defining behavior and display of 
    UserProfileInfos in the Django admin interface.
    """
    fieldsets: tuple[tuple[str, dict[str, tuple[str]]]] = (
        ('General', {
            'fields': (
                'hidden_from_public',
                'minecraft_username',
                'favorite_modpack')
        }),
        ('Profile Picture', {
            'classes': ('collapse',),
            'fields': ('profile_picture','picture_changed_manually')
        })
    )

    readonly_fields: tuple[str] = (
        'picture_changed_manually',
    )

    search_fields: list[str] = [
        'minecraft_username',
    ]


class DiscordUserInfoAdmin(admin.ModelAdmin):
    """
    Object defining behavior and display of 
    DiscordUserInfos in the Django admin interface.
    """
    fieldsets: tuple[tuple[str, dict[str, tuple[str]]]] = (
        ('General', {
            'fields': (
                'tag',
                'avatar_string',
                'pub_flags',
                'flags',
                'locale')
        }),
        ('Sensitive', {
            'classes': ('collapse',),
            'fields': ('id','mfa_enabled')
        })
    )

    readonly_fields: tuple[str] = (
        'id',
        'mfa_enabled',
        'pub_flags',
        'flags',
        'locale',
    )

    search_fields: list[str] = [
        'tag',
    ]


class DeletionQueueForUserAdmin(admin.ModelAdmin):
    """
    Object defining behavior and display of 
    UserDeleteQueue in the Django admin interface.
    """
    fieldsets: tuple[tuple[str, dict[str, tuple[str]]]] = (
        ('General', {
            'fields': (
                'user',)
        }),
    )

    readonly_fields: tuple[str] = (
        'user',
    )

    list_display: list[str] = ['user']


admin.site.unregister(Group)

admin.site.register(RaptorUser, RaptorUserAdmin)
admin.site.register(UserProfileInfo, UserProfileInfoAdmin)
admin.site.register(DiscordUserInfo, DiscordUserInfoAdmin)
admin.site.register(DeletionQueueForUser, DeletionQueueForUserAdmin)
