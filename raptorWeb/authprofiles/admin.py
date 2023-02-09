from django import forms
from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin

from raptorWeb.authprofiles.models import RaptorUser, UserProfileInfo, DiscordUserInfo

class RaptorUserAdminForm(forms.ModelForm):
    class Meta:
        model = RaptorUser
        widgets = {
            'password': forms.PasswordInput()
        }
        fields = '__all__'

class RaptorUserAdmin(UserAdmin):
    fieldsets = (
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
            'fields': ('is_superuser', 'is_staff', 'password')
        })
    )

    readonly_fields = (
        'is_discord_user',
        'date_joined',
        'last_login',
        'user_profile_info',
        'discord_user_info'
    )

    search_fields = [
        'username',
        'user_slug',
        'email',
        'discord_user_info__tag'
    ]

    list_display = ['username', 'email', 'is_discord_user', 'is_staff', 'is_active', 'date_joined']

    filter_horizontal = ('user_permissions', 'groups')

admin.site.unregister(User)
admin.site.unregister(Group)

admin.site.register(RaptorUser, RaptorUserAdmin)
admin.site.register(UserProfileInfo)
admin.site.register(DiscordUserInfo)
