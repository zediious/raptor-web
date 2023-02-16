from django.contrib import admin
from django.forms import ModelForm
from django.forms import TextInput, Textarea
from django.db import models

from tinymce.widgets import TinyMCE

from raptorWeb.raptormc.models import InformativeText, SiteInformation, NavbarLink, NavbarDropdown


class InformativeTextAdminForm(ModelForm):
    class Meta:
        model = InformativeText
        widgets = {
            'content': TinyMCE
        }
        fields = '__all__'

class SiteInformationAdminForm(ModelForm):
    class Meta:
        model = SiteInformation
        widgets = {
            'main_color': TextInput(attrs={'type': 'color'}),
            'secondary_color': TextInput(attrs={'type': 'color'})
        }
        fields = '__all__'


class NavbarDropdownAdmin(admin.ModelAdmin):
    """
    Object defining behavior and display of 
    NavbarDropdowns in the Django admin interface.
    """
    fieldsets: tuple[tuple[str, dict[str, tuple[str]]]] = (
        ('Navigation Link', {
            'fields': (
                'enabled',
                'priority',
                'name')
        }),
    )

    search_fields: list[str] = [
        'name',
    ]

    list_display: list[str] = ['name', 'priority', 'enabled']


class NavbarLinkAdmin(admin.ModelAdmin):
    """
    Object defining behavior and display of 
    NavbarLinks in the Django admin interface.
    """
    fieldsets: tuple[tuple[str, dict[str, tuple[str]]]] = (
        ('Navigation Link', {
            'fields': (
                'enabled',
                'priority',
                'parent_dropdown',
                'new_tab',
                'name',
                'url')
        }),
    )

    search_fields: list[str] = [
        'name',
        'url'
    ]

    list_display: list[str] = ['name', 'url', 'parent_dropdown', 'priority', 'enabled']


class InformativeTextAdmin(admin.ModelAdmin):
    """
    Object defining behavior and display of 
    InformativeTexts in the Django admin interface.
    """
    form = InformativeTextAdminForm

    fieldsets: tuple[tuple[str, dict[str, tuple[str]]]] = (
        ('Informative Text', {
            'fields': (
                'enabled',
                'name',
                'content')
        }),
    )

    readonly_fields: tuple[str] = (
        'name',
    )

    search_fields: list[str] = [
        'name',
    ]

    list_display: list[str] = ['name', 'enabled']

    def has_add_permission(self, request, obj=None):
        return False


class SiteInformationAdmin(admin.ModelAdmin):
    """
    Object defining behavior and display of 
    SiteInformations in the Django admin interface.
    """
    form = SiteInformationAdminForm

    fieldsets: tuple[tuple[str, dict[str, tuple[str]]]] = (
        ('Information', {
            'fields': (
                'brand_name',)
        }),
        ('Colors', {
            'fields': (
                'main_color',
                'secondary_color')
        }),
        ('Images', {
            'fields': (
                'branding_image',
                'background_image')
        })
    )

    list_display: list[str] = [
        'brand_name',
        'main_color',
        'secondary_color',
        'branding_image',
        'background_image']

    def has_add_permission(self, request, obj=None):
        return False


admin.site.register(InformativeText, InformativeTextAdmin)
admin.site.register(SiteInformation, SiteInformationAdmin)
admin.site.register(NavbarLink, NavbarLinkAdmin)
admin.site.register(NavbarDropdown, NavbarDropdownAdmin)
