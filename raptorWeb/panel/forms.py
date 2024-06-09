from logging import getLogger

from django import forms
from django.utils.safestring import mark_safe

from tinymce.widgets import TinyMCE

from raptorWeb.raptormc.models import SiteInformation, DefaultPages, InformativeText, Page, NotificationToast, NavWidget
from raptorWeb.donations.models import DonationPackage
from raptorWeb.staffapps.models import CreatedStaffApplication
from raptorWeb.authprofiles.models import RaptorUser, UserProfileInfo, DiscordUserInfo, RaptorUserGroup
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
        
        
class PanelServerCreateForm(forms.ModelForm):
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
            'rcon_password': forms.PasswordInput
        }


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
            'modpack_picture': PictureWidget,
            'rcon_password': forms.PasswordInput(render_value = True)
        }


class PanelPlayerFilterForm(forms.Form):
    """
    Form returned to filter the player list
    """
    username: forms.CharField = forms.CharField(
        label="Username",
        required=False
    )
    
    
class PanelPlayerPaginateForm(forms.Form):
    """
    Form returned to choose amount of players on each page
    """   
    paginate_by: forms.IntegerField = forms.IntegerField(
        label='Items per Page',
        required=False
    )


class PanelInformativeTextUpdateForm(forms.ModelForm):
    class Meta:
        model = InformativeText
        fields = (
        'content',
        'enabled',)
        widgets = {
            'content': TinyMCE(attrs={'cols': 80, 'rows': 30})
        }
        
        
class PanelPageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = (
        'name',
        'content',
        'meta_description',
        'meta_keywords',
        'page_css',
        'page_js',)
        widgets = {
            'content': TinyMCE(attrs={'cols': 80, 'rows': 30})
        }
        

class PanelToastForm(forms.ModelForm):
    class Meta:
        model = NotificationToast
        fields = (
        'name',
        'message',
        'enabled',)
        widgets = {
            'message': TinyMCE(attrs={'cols': 80, 'rows': 30})
        }
        
        
class PanelNavWidgetUpdateForm(forms.ModelForm):
    class Meta:
        model = NavWidget
        fields = (
        'name',
        'url',
        'linked_page',
        'parent_bar',
        'nav_image',
        'tooltip',
        'priority',
        'new_tab',
        'enabled',)
        widgets = {
            'nav_image': PictureWidget
        }
        
        
class PanelNavWidgetCreateForm(forms.ModelForm):
    class Meta:
        model = NavWidget
        fields = (
        'name',
        'url',
        'linked_page',
        'parent_bar',
        'nav_image',
        'tooltip',
        'priority',
        'new_tab',
        'enabled',)
        
        
class PanelDonationPackageUpdateForm(forms.ModelForm): 
    class Meta:
        model = DonationPackage
        fields: str = "__all__"
        widgets = {
            'package_description': TinyMCE(attrs={'cols': 80, 'rows': 30}),
            'package_picture': PictureWidget,
            'servers': forms.CheckboxSelectMultiple,
            'commands': forms.CheckboxSelectMultiple,
            'discord_roles': forms.CheckboxSelectMultiple
        }
        
        
class PanelDonationPackageCreateForm(forms.ModelForm):
    price = forms.IntegerField(
        required=True,
        min_value=1
    )
    
    class Meta:
        model = DonationPackage
        fields: str = "__all__"
        widgets = {
            'package_description': TinyMCE(attrs={'cols': 80, 'rows': 30}),
            'servers': forms.CheckboxSelectMultiple,
            'commands': forms.CheckboxSelectMultiple,
            'discord_roles': forms.CheckboxSelectMultiple
        }
        
        
class PanelCreatedStaffApplicationForm(forms.ModelForm): 
    class Meta:
        model = CreatedStaffApplication
        fields: str = "__all__"
        widgets = {
            'form_fields': forms.CheckboxSelectMultiple
        }
        
        
class PanelUserUpdateForm(forms.ModelForm): 
    password = forms.CharField(
        required=False
    )
    
    user_slug = forms.CharField(
        required=False
    )
    
    date_joined = forms.CharField(
        required=False
    )
    
    last_login = forms.CharField(
        required=False
    )
    
    class Meta:
        model = RaptorUser
        exclude = (
            'id',
            'password',
            'totp_token',
            'totp_qr_path',
            'user_slug',
            'date_joined',
            'last_login',
            'is_discord_user',
            'date_queued_for_delete',
            'user_profile_info',
            'discord_user_info',
        )
        widgets = {
            'user_permissions': forms.CheckboxSelectMultiple,
            'groups': forms.CheckboxSelectMultiple
        }
        
        
class PanelUserProfileInfoUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfileInfo
        fields = (
        'hidden_from_public',
        'minecraft_username',
        'favorite_modpack',
        'profile_picture',)
        widgets = {
            'profile_picture': PictureWidget
        }


class PanelDiscordUserInfoUpdateForm(forms.ModelForm):
    class Meta:
        model = DiscordUserInfo
        exclude = (
            'id',
            'tag',
            'pub_flags',
            'flags',
            'locale',
            'mfa_enabled',
        )
        
        
class PanelRaptorUserGroupForm(forms.ModelForm): 
    class Meta:
        model = RaptorUserGroup
        fields = [
            'name',
            'permissions'
        ]
        widgets = {
            'permissions': forms.CheckboxSelectMultiple
        }
        