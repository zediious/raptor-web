from django import forms

from raptorWeb.raptormc.models import SiteInformation, DefaultPages


class PanelSettingsInformation(forms.ModelForm):
    """
    Form for editing site information
    """
    brand_name: forms.CharField = forms.CharField(
        help_text="The name of your website and/or network",
        widget=forms.TextInput(),
        required=False),
    
    contact_email: forms.EmailField = forms.EmailField(
        help_text="Email to be linked with a mailto in the footer of the website.",
        widget=forms.EmailInput(),
        required=False)
    
    main_color: forms.CharField = forms.CharField(
        help_text="The hex color code used for the lower body of the website",
        widget=forms.TextInput(attrs={'type': 'color'}),
        required=False)
    
    use_main_color: forms.BooleanField = forms.BooleanField(
        help_text="If this is checked, the Main Color chosen above will be used on the website.",
        required=False)
    
    secondary_color: forms.CharField = forms.CharField(
        help_text=("The hex color code used for the upper body of the website, layered "
                    "underneath server buttons"),
        widget=forms.TextInput(attrs={'type': 'color'}),
        required=False)
    
    use_secondary_color: forms.BooleanField = forms.BooleanField(
        help_text=("If this is checked, the Secondary Color chosen above will be used on the website. If "
                   "you are using a Background Image, that will always take precedence."),
        required=False)
    
    meta_description: forms.CharField = forms.CharField(
        help_text=("The description for your website provided in search engine results. "
                    "This will apply to all pages that do not override."),
        required=False)
    
    meta_keywords: forms.CharField = forms.CharField(
        help_text=("A series of comma-separated values that represent meta keywords used "
                    "in search engine results. This will apply to all pages that do not override."),
        required=False)
    
    enable_footer: forms.BooleanField = forms.BooleanField(
        help_text=("If this is checked, the footer will be enabled"),
        required=False)
    
    enable_footer_credit: forms.BooleanField = forms.BooleanField(
        help_text=("If this is checked, the footer will be enabled"),
        required=False)
    
    enable_footer_contact: forms.BooleanField = forms.BooleanField(
        help_text=("If this is checked, the footer will be enabled"),
        required=False)
    
    require_login_for_user_list: forms.BooleanField = forms.BooleanField(
        help_text=("If this is checked, users will need to create an account and, "
                   "log in before they can access the Site Members list."),
        required=False)
    
    enable_server_query: forms.BooleanField = forms.BooleanField(
         help_text=("If this is un-checked, the address/port of created Servers will NOT be, "
                   "queried for state and player data. Each server's information will still be "
                   "displayed on the website as normal, however the Player Counts section "
                   "of the Header Box will no longer appear."),
        required=False)

    class Meta():
        model: SiteInformation = SiteInformation
        fields: tuple[str] = (
            'brand_name',
            'contact_email',
            'main_color',
            'use_main_color',
            'secondary_color',
            'use_secondary_color',
            'meta_description',
            'meta_keywords',
            'enable_footer',
            'enable_footer_credit',
            'enable_footer_contact',
            'require_login_for_user_list',
            'enable_server_query'
            )
        
        
class PanelSettingsFiles(forms.ModelForm):
    """
    Form for editing site files
    """  
    branding_image: forms.ImageField = forms.ImageField(
        help_text=("The image displayed in the website Navigation Bar as a link to the "
                    "homepage. Optimal size for this image is w800xh200."),
        required=False)
    
    background_image: forms.ImageField = forms.ImageField(
        help_text=("The image displayed layered behind server buttons. This image will "
                    "cover the defined Secondary Color if used. Optimal size for this image "
                    " is 1920x1080 or within the same aspect ratio."),
        required=False)
    
    avatar_image: forms.ImageField = forms.ImageField(
        help_text=("The image displayed in OpenGraph embeds, such as when a link is " 
                   "pasted to a Discord Channel or a Twitter post. This should be a 1x1 image. "
                   "This will also be used as your Favicon, after being converted to a .ico file."),
        required=False)

    class Meta():
        model: SiteInformation = SiteInformation
        fields: tuple[str] = (
            'branding_image',
            'background_image',
            'avatar_image'
            )
        
        
class PanelDefaultPages(forms.ModelForm):
    """
    Form for editing default page enabled states
    """  
    announcements : forms.BooleanField = forms.BooleanField(
        help_text="Whether the default Announcement page is enabled or not",
        required=False)
    
    rules: forms.BooleanField = forms.BooleanField(
        help_text="Whether the default Rules page is enabled or not",
        required=False)
    
    banned_items: forms.BooleanField = forms.BooleanField(
        help_text="Whether the default Banned Items page is enabled or not",
        required=False)
    
    voting: forms.BooleanField = forms.BooleanField(
        help_text="Whether the default Voting page is enabled or not",
        required=False)
    
    joining: forms.BooleanField = forms.BooleanField(
        help_text="Whether the default Joining page is enabled or not",
        required=False)
    
    staff_apps: forms.BooleanField = forms.BooleanField(
        help_text="Whether the default Staff Applications page is enabled or not",
        required=False)
    
    members: forms.BooleanField = forms.BooleanField(
        help_text=("Whether the default Member List, page is enabled or not. This will "
                   "also disable access to user profile pages, unless a user is logged in "
                   "to view their own profile."),
        required=False)

    class Meta():
        model: DefaultPages = DefaultPages
        fields: tuple[str] = (
            'announcements',
            'rules',
            'banned_items',
            'voting',
            'joining',
            'staff_apps',
            'members'
            )

