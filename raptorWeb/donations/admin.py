from django.contrib import admin
from django.forms import ModelForm

from tinymce.widgets import TinyMCE

from raptorWeb.donations.models import DonationPackage, DonationServerCommand, DonationDiscordRole

class DonationPackageAdminForm(ModelForm):
    class Meta:
        model = DonationPackage
        widgets = {
            'package_description': TinyMCE
        }
        fields = '__all__'


class DonationPackageAdmin(admin.ModelAdmin):
    """
    Object defining behavior and display of 
    Donation Packages in the Django admin interface.
    """
    form = DonationPackageAdminForm
    
    fieldsets: tuple[tuple[str, dict[str, tuple[str]]]] = (
        ('Package Information', {
            'fields': (
                'name',
                'price',
                'variable_price',
                'allow_repeat',
                'priority',
                'package_picture',
                'package_description')
        }),
        ('Benefits', {
            'fields': (
                'servers',
                'commands',
                'discord_roles',)
        }),
    )

    search_fields: list[str] = [
        'name',
    ]

    list_display: list[str] = ['name', 'allow_repeat', 'variable_price', 'price', 'priority']
    
    
class DonationServerCommandAdmin(admin.ModelAdmin):
    """
    Object defining behavior and display of Donation
    Server Commands in the Django admin interface.
    """
    fieldsets: tuple[tuple[str, dict[str, tuple[str]]]] = (
        ('Donation Command', {
            'fields': (
                'command',)
        }),
    )

    search_fields: list[str] = [
        'command',
    ]

    list_display: list[str] = ['command']
    
    
class DonationDiscordroleAdmin(admin.ModelAdmin):
    """
    Object defining behavior and display of Donation
    Discord Roles in the Django admin interface.
    """
    fieldsets: tuple[tuple[str, dict[str, tuple[str]]]] = (
        ('Discord Role', {
            'fields': (
                'name',
                'role_id')
        }),
    )

    search_fields: list[str] = [
        'name',
        'role_id,'
    ]

    list_display: list[str] = ['name', 'role_id']
    
admin.site.register(DonationPackage, DonationPackageAdmin)
admin.site.register(DonationServerCommand, DonationServerCommandAdmin)
admin.site.register(DonationDiscordRole, DonationDiscordroleAdmin)
