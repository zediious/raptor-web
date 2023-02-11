from django import forms
from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin

from raptorWeb.authprofiles.models import RaptorUser, UserProfileInfo, DiscordUserInfo

class RaptorUserAdminForm(forms.ModelForm):
    class Meta:
        model = RaptorUser
        widgets: dict = {
            'password': forms.PasswordInput()
        }
        fields: str = '__all__'

class RaptorUserAdmin(UserAdmin):
    fieldsets: tuple[tuple] = (
        ('General', {
            'fields': (
                'user_profile_info',
                'discord_user_info',
                'is_active',
                'is_discord_user',
                'email',
                'first_name',
                'last_name',
                'username',
                'user_slug',
                'date_joined',
                'last_login')
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

    list_display = ['username', 'email', 'is_discord_user', 'is_staff', 'is_active', 'date_joined']

admin.site.unregister(Group)

admin.site.register(RaptorUser, RaptorUserAdmin)
admin.site.register(UserProfileInfo)
admin.site.register(DiscordUserInfo)
