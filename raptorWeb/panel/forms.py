from logging import getLogger

from django import forms
from django.utils.safestring import mark_safe

from tinymce.widgets import TinyMCE

from raptorWeb.raptormc.models import SiteInformation, DefaultPages
from raptorWeb.gameservers.models import Server

LOGGER = getLogger('panel.forms')


class PictureWidget(forms.widgets.FileInput):
    """
    Widget to display image in ImageFields when returned in forms
    along with option to upload new image
    """
    def render(self, name, value, attrs=None, **kwargs):
        input_html = super().render(name, value, attrs=None, **kwargs)
        try:    
            img_html = mark_safe(f'<br><br><img class="panel-modpack-image mb-3" src="{value.url}"/>')
            
        except ValueError:
            return mark_safe(f'{input_html}')
        
        return mark_safe(f'{input_html}{img_html}')


class PanelSettingsInformation(forms.ModelForm):
    """
    Form for editing site information
    """
    class Meta():
        model: SiteInformation = SiteInformation
        fields: str = "__all__"
        widgets = {
            'main_color': forms.TextInput(attrs={'type': 'color'}),
            'secondary_color': forms.TextInput(attrs={'type': 'color'}),
        }
        exclude: tuple[str] = (
            'branding_image',
            'branding_image_svg',
            'background_image',
            'avatar_image',
            'donation_goal_progress'
            )
        
        
class PanelSettingsFiles(forms.ModelForm):
    """
    Form for editing site files
    """   
    remove_branding_image: forms.BooleanField = forms.BooleanField(
        help_text=("If this is checked, the current Branding Image will be cleared "),
        required=False)
    
    remove_background_image: forms.BooleanField = forms.BooleanField(
        help_text=("If this is checked, the current Background Image will be cleared "),
        required=False)
    
    remove_avatar_image: forms.BooleanField = forms.BooleanField(
        help_text=("If this is checked, the current Avatar Image will be cleared "),
        required=False)

    class Meta():
        model: SiteInformation = SiteInformation
        fields: tuple[str] = (
            'branding_image',
            'branding_image_svg',
            'background_image',
            'avatar_image',
            )
        
        
class PanelDefaultPages(forms.ModelForm):
    """
    Form for editing default page enabled states
    """  
    class Meta():
        model: DefaultPages = DefaultPages
        fields: str = '__all__'


class PanelServerUpdateForm(forms.ModelForm):
    class Meta:
        model = Server
        fields = (
        'modpack_name',
        'modpack_version',
        'server_address',
        'server_port',
        'modpack_url',
        'modpack_picture',
        'discord_announcement_channel_id',
        'discord_modpack_role_id',
        'rcon_address',
        'rcon_port',
        'rcon_password',
        'modpack_description',
        'server_description',
        'server_rules',
        'server_banned_items',
        'server_vote_links',)
        widgets = {
            'modpack_description': TinyMCE(attrs={'cols': 80, 'rows': 30}),
            'server_description': TinyMCE(attrs={'cols': 80, 'rows': 30}),
            'server_rules': TinyMCE(attrs={'cols': 80, 'rows': 30}),
            'server_banned_items': TinyMCE(attrs={'cols': 80, 'rows': 30}),
            'server_vote_links': TinyMCE(attrs={'cols': 80, 'rows': 30}),
            'modpack_picture': PictureWidget
        }

