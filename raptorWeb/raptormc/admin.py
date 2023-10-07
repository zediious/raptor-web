from django.contrib import admin
from django.forms import ModelForm
from django.forms import TextInput

from tinymce.widgets import TinyMCE

from raptorWeb.raptormc.models import InformativeText, SiteInformation, NavbarLink, NavbarDropdown, NavWidget, NavWidgetBar, NotificationToast, Page, DefaultPages


class PageAdminForm(ModelForm):
    class Meta:
        model = Page
        widgets = {
            'content': TinyMCE
        }
        fields = '__all__'


class NotificationToastAdminForm(ModelForm):
    class Meta:
        model = NotificationToast
        widgets = {
            'message': TinyMCE
        }
        fields = '__all__'


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


class PageAdmin(admin.ModelAdmin):
    """
    Object defining behavior and display of 
    Pages in the Django admin interface.
    """
    form = PageAdminForm

    fieldsets: tuple[tuple[str, dict[str, tuple[str]]]] = (
        ('Page Content', {
            'fields': (
                'name',
                'content')
        }),
        ('CSS/JS', {
            'fields': (
                'page_css',
                'page_js')
        }),
        ('SEO', {
            'fields': (
                'meta_description',
                'meta_keywords')
        }),
        ('Misc', {
            'fields': (
                'show_gameservers',
                'created')
        })
    )

    readonly_fields: tuple[str] = (
        'created',
    )

    search_fields: list[str] = [
        'name'
    ]

    list_display: list[str] = ['name', 'created', 'show_gameservers']
    
    
class DefaultPageAdmin(admin.ModelAdmin):
    """
    Object tracking enabled state of default pages
    """
    list_display: list[str] = ['announcements', 'rules', 'banned_items', 'voting', 'joining', 'staff_apps', 'members']
    
    def has_add_permission(self, request, obj=None):
        return False


class NotificationToastAdmin(admin.ModelAdmin):
    """
    Object defining behavior and display of 
    NotificationToasts in the Django admin interface.
    """
    form = NotificationToastAdminForm

    fieldsets: tuple[tuple[str, dict[str, tuple[str]]]] = (
        ('Notification Toast', {
            'fields': (
                'enabled',
                'name',
                'message',
                'created')
        }),
    )

    readonly_fields: tuple[str] = (
        'created',
    )

    search_fields: list[str] = [
        'name'
    ]

    list_display: list[str] = ['name', 'created', 'enabled']


class NavWidgetBarAdmin(admin.ModelAdmin):
    """
    Object defining behavior and display of 
    NavWidgetBars in the Django admin interface.
    """
    fieldsets: tuple[tuple[str, dict[str, tuple[str]]]] = (
        ('Nav Widget Bar', {
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


class NavWidgetAdmin(admin.ModelAdmin):
    """
    Object defining behavior and display of 
    NavWidgets in the Django admin interface.
    """
    fieldsets: tuple[tuple[str, dict[str, tuple[str]]]] = (
        ('Nav Widget', {
            'fields': (
                'enabled',
                'priority',
                'parent_bar',
                'linked_page',
                'new_tab',
                'name',
                'nav_image',
                'url')
        }),
    )

    search_fields: list[str] = [
        'name',
        'url'
    ]

    list_display: list[str] = ['name', 'url', 'parent_bar', 'priority', 'enabled']


class NavbarDropdownAdmin(admin.ModelAdmin):
    """
    Object defining behavior and display of 
    NavbarDropdowns in the Django admin interface.
    """
    fieldsets: tuple[tuple[str, dict[str, tuple[str]]]] = (
        ('Navigation Dropdown', {
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
                'linked_page',
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
                'brand_name',
                'contact_email')
        }),
        ('Colors', {
            'fields': (
                'main_color',
                'use_main_color',
                'secondary_color',
                'use_secondary_color')
        }),
        ('Images', {
            'fields': (
                'branding_image',
                'background_image',
                'avatar_image')
        }),
        ('SEO', {
            'fields': (
                'meta_description',
                'meta_keywords')
        }),
         ('Misc', {
            'fields': (
                'enable_footer',
                'enable_footer_credit',
                'enable_footer_contact')
        })
    )

    list_display: list[str] = [
        'brand_name',
        'main_color',
        'secondary_color',
        'branding_image',
        'background_image',
        'avatar_image']

    def has_add_permission(self, request, obj=None):
        return False


admin.site.register(InformativeText, InformativeTextAdmin)
admin.site.register(SiteInformation, SiteInformationAdmin)
admin.site.register(NavbarLink, NavbarLinkAdmin)
admin.site.register(NavbarDropdown, NavbarDropdownAdmin)
admin.site.register(NavWidget, NavWidgetAdmin)
admin.site.register(NavWidgetBar, NavWidgetBarAdmin)
admin.site.register(NotificationToast, NotificationToastAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(DefaultPages, DefaultPageAdmin)
