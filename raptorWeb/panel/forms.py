from logging import getLogger

from django import forms

from raptorWeb.raptormc.models import SiteInformation, DefaultPages

LOGGER = getLogger('panel.forms')


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
            'avatar_image'
            )
        
        
class PanelDefaultPages(forms.ModelForm):
    """
    Form for editing default page enabled states
    """  
    class Meta():
        model: DefaultPages = DefaultPages
        fields: str = '__all__'

