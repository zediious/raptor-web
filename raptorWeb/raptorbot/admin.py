from django.contrib import admin
from django.forms import ModelForm

from tinymce.widgets import TinyMCE

from raptorWeb.raptorbot.models import DiscordGuild, GlobalAnnouncement, ServerAnnouncement


class AnnouncementForm(ModelForm):
    class Meta:
        model = GlobalAnnouncement
        widgets = {
            'message': TinyMCE,
        }
        fields = '__all__'


class GlobalAnnouncementAdmin(admin.ModelAdmin):
    """
    Object defining behavior and display of 
    GlobalAnnouncements in the Django admin interface.
    """
    form = AnnouncementForm

    fieldsets: tuple[tuple[str, dict[str, tuple[str]]]] = (
        ('General', {
            'fields': (
                'author',
                'date',
                'message')
        }),
    )

    readonly_fields: tuple[str] = (
        'date',
    )

    search_fields: list[str] = [
        'author',
        'message',
    ]

    list_display: list[str] = ['author', 'date']

class ServerAnnouncementAdmin(admin.ModelAdmin):
    """
    Object defining behavior and display of 
    ServerAnnouncements in the Django admin interface.
    """
    form = AnnouncementForm
    
    fieldsets: tuple[tuple[str, dict[str, tuple[str]]]] = (
        ('General', {
            'fields': (
                'server',
                'author',
                'date',
                'message')
        }),
    )

    readonly_fields: tuple[str] = (
        'date',
        'server'
    )

    search_fields: list[str] = [
        'author',
        'message',
    ]

    list_display: list[str] = ['author', 'date', 'server']


admin.site.register(GlobalAnnouncement, GlobalAnnouncementAdmin)
admin.site.register(ServerAnnouncement, ServerAnnouncementAdmin)
