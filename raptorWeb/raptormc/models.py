from re import sub
from logging import Logger, getLogger

from django.db import models
from django.utils.text import slugify
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from django.core.validators import MaxValueValidator, MinValueValidator

from django_resized import ResizedImageField

LOGGER: Logger = getLogger('raptormc.models')

class PageManager(models.Manager):
    """
    Manager for Page objects
    """
    def get_slugged_page(self, page_name):
        """
        Given a page name, find a page whose name attribute
        matches the slugged page name after both paraneters
        have been slugified.
        """
        for page in self.all():
            if slugify(page.name) == slugify(page_name):
                return page


class Page(models.Model):
    """
    A new webpage with a Title and Content. This page will extend to entire
    base website, but you can choose whether to include Server buttons or not.
    """
    objects = PageManager()

    name = models.CharField(
        max_length=100,
        verbose_name="Name",
        help_text="The name of this page, will be displayed at the top, before the page content."
    )

    content = models.TextField(
        max_length=15000,
        default = "",
        verbose_name="Content",
        help_text="The content of this page."
    )

    created = models.DateTimeField(
        auto_now_add=True
    )

    show_gameservers = models.BooleanField(
        default=True,
        verbose_name="Show Servers",
        help_text="If this is checked, this page will display Server buttons in the usual location."
    )
    
    meta_description = models.CharField(
        max_length=500,
        default="",
        blank=True,
        verbose_name="SEO Description",
        help_text=("The description for this page provided in search engine results. "
                    "This will apply only to this page, overriding default."),
    )
    
    meta_keywords = models.CharField(
        max_length=500,
        default="",
        blank=True,
        verbose_name="SEO Keywords",
        help_text=("The comma-separated keywords for this page used in search engine results. "
                    "This will apply only to this page, overriding default."),
    )
    
    page_css = models.FileField(
        upload_to='page_css',
        verbose_name="Page CSS",
        help_text=("Custom style sheet that will only apply on this page. "
                    "This will apply only to this page, overriding any defaults."),
        blank=True
    )
    
    page_js = models.FileField(
        upload_to='page_js',
        verbose_name="Page JavaScript",
        help_text=("Custom Javascript that will only apply on this page."),
        blank=True
    )

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return f"/pages/{slugify(self.name)}"

    class Meta:
        verbose_name = "Page",
        verbose_name_plural = "Pages"


class NotificationToast(models.Model):
    """
    A Notification/Toast that will appear on the bottom right of the website.
    Users will only see these messages once, until their session expires.
    """
    enabled = models.BooleanField(
        default=True,
        verbose_name="Enabled",
        help_text="Whether this Notification will appear on the website"
    )

    name = models.CharField(
        max_length=100,
        verbose_name="Notification Name",
        help_text="The title of this notification that will appear on the website"
    )

    message = models.CharField(
        max_length=15000,
        default = "",
        verbose_name="Message",
        help_text="The message for this notification"
    )

    created = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Notification Toast",
        verbose_name_plural = "Notification Toasts"


class NavWidgetBar(models.Model):
    """
    A bar at the top of the website that contains Widgets.
    Newly added bars will always appear below the default bar.
    """
    name = models.CharField(
        max_length=100,
        verbose_name="Nav Widget Bar Name",
        help_text=("The name of this Nav Widget Bar. Only used for internal identification."),
        default="Default"
    )

    enabled = models.BooleanField(
        verbose_name="Enabled",
        help_text="Whether this Nav Widget Bar will appear on the website.",
        default=True
    )

    priority = models.IntegerField(
        verbose_name="Priority",
        help_text="Controls the order this Nav Widget Bar will be placed in. Lower numbers appear first.",
        default=0
    )

    def __str__(self):
        return str(self.name)

    def enabled_links_in_widgetbar(self):
        return self.nestednavwidget.filter(enabled=True).order_by('priority')

    class Meta:
        verbose_name = "Nav Widget Bar",
        verbose_name_plural = "Nav Widget Bars"


class NavWidget(models.Model):
    """
    A Navigation Button that appears at the very top of the website, alongside the Discord widget.
    """
    name = models.CharField(
        max_length=100,
        verbose_name="Navigation Link Name",
        help_text=("The name of this Navigation Button. Will be displayed on the website. "
                    "if a Widget Image is not used."),
        default="Default"
    )
    
    tooltip = models.CharField(
        max_length=300,
        verbose_name="Widget Tooltip",
        help_text=("A tooltip with custom text that will be displayed when the widget is "
                    "hovered over, or held down on a touchscreen."),
        default="",
        blank=True
    )

    nav_image = ResizedImageField(
        upload_to='navwidgetimage',
        verbose_name="Nav Widget Image",
        help_text=("The image used as an identifier/name for this Nav Widget. "
                    "Optimal size for this image is w250xh72 or within the same aspect ratio."),
        blank=True,
        size=[250,72],
        quality=50,
        force_format='WEBP',
        keep_meta=False
    )

    url = models.URLField(
        max_length=250,
        verbose_name="Navigation URL",
        help_text="The link this Navigation button will take the user to.",
        default="https://google.com"
    )

    enabled = models.BooleanField(
        verbose_name="Enabled",
        help_text="Whether this Navigation Button will appear on the website.",
        default=True
    )

    priority = models.IntegerField(
        verbose_name="Priority",
        help_text="Controls the order this Navigation Button will be placed in. Lower numbers appear first.",
        default=0
    )

    new_tab = models.BooleanField(
        verbose_name="Opens in New Tab",
        help_text="If this is True, this Button will open in a new tab.",
        default=False
    )

    linked_page = models.ForeignKey(
        Page,
        verbose_name="Linked Page",
        help_text="The Page Model that this Navigation Button will lead to. If this is set, then the Navigation URL field will be ignored.",
        related_name='widgettopage',
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING
    )

    parent_bar = models.ForeignKey(
        NavWidgetBar,
        verbose_name="Linked Nav Widget Bar",
        help_text="The Nav Widget Bar this link is attached to. A Nav Widget will appear in the default Nav Widget Bar. "
                 "if one is not specified here",
        related_name='nestednavwidget',
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Nav Widget",
        verbose_name_plural = "Nav Widgets"


class NavbarDropdown(models.Model):
    """
    A Dropdown Menu for the Navigation sidebar. Add Links to a Dropdown
    Menu from within a Navigation Link's configuration.
    """
    name = models.CharField(
        max_length=100,
        verbose_name="Navigation Link Name",
        help_text=("The name of this Navigation Dropdown. Will be displayed on the website."),
        default="Default"
    )

    enabled = models.BooleanField(
        verbose_name="Enabled",
        help_text="Whether this Navigation Link will appear on the website.",
        default=True
    )

    priority = models.IntegerField(
        verbose_name="Priority",
        help_text="Controls the order this Navigation Dropdown will be placed in. Lower numbers appear first.",
        default=0
    )

    def __str__(self):
        return str(self.name)

    def enabled_links_in_dropdown(self):
        return self.nestedlink.filter(enabled=True).order_by('priority')

    class Meta:
        verbose_name = "Navigation Drodown",
        verbose_name_plural = "Navigation Dropdowns"


class NavbarLink(models.Model):
    """
    A Navigation Link which will be added to the Navigation sidebar. Can be placed inside
    of a created Dropdown Menu.
    """
    name = models.CharField(
        max_length=100,
        verbose_name="Navigation Link Name",
        help_text=("The name of this Navigation Link. Will be displayed on the website."),
        default="Default"
    )

    url = models.URLField(
        max_length=250,
        verbose_name="Navigation URL",
        help_text="The link this Navigation Link will take the user to.",
        default="https://google.com"
    )

    enabled = models.BooleanField(
        verbose_name="Enabled",
        help_text="Whether this Navigation Link will appear on the website.",
        default=True
    )

    priority = models.IntegerField(
        verbose_name="Priority",
        help_text="Controls the order this Navigation Link will be placed in. Lower numbers appear first.",
        default=0
    )

    new_tab = models.BooleanField(
        verbose_name="Opens in New Tab",
        help_text="If this is True, this link will open in a new tab.",
        default=False
    )

    linked_page = models.ForeignKey(
        Page,
        verbose_name="Linked Page",
        help_text="The Page Model that this Navigation Link will lead to. If this is set, then the Navigation URL field will be ignored.",
        related_name='linktopage',
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING
    )

    parent_dropdown = models.ForeignKey(
        NavbarDropdown,
        verbose_name="Dropdown Menu",
        help_text="The Dropdown Menu this link is attached to. This is not required",
        related_name='nestedlink',
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING
    )

    def __str__(self):
        return str(self.name)

    def get_linked_page_url(self):
        return self.linked_page.get_absolute_url()

    class Meta:
        verbose_name = "Navigation Link",
        verbose_name_plural = "Navigation Links"


class SiteInformation(models.Model):
    """
    Settings model for the application. Contains most settings that the
    user would change from the user interface in regards to how the
    application behaves and/or looks.
    """
    brand_name = models.CharField(
        max_length=100,
        verbose_name="Website/Network Name",
        help_text=("The name of your website and/or network"),
        default="Default"
    )
    
    contact_email = models.EmailField(
        max_length=500,
        verbose_name="Contact Email",
        help_text=("Email to be linked with a mailto link in the footer of the website."),
        blank=True,
        default=""
    )

    main_color = models.CharField(
        max_length=7,
        verbose_name="Main Color",
        help_text="The hex color code used for the lower body of the website",
        default="#00192d"
    )

    secondary_color = models.CharField(
        max_length=7,
        verbose_name="Secondary Color",
        help_text=("The hex color code used for the upper body of the website, layered "
                    "underneath server buttons. If using a Background Image, that will "
                    "always override this color."),
        default="#00233c"
    )

    branding_image = ResizedImageField(
        upload_to='branding',
        verbose_name="Branding Image",
        help_text=("The image displayed in the website Navigation Bar as a link to the "
                    "homepage. Image will be resized to 550x170 after uploading."),
        blank=True,
        size=[550,170],
        quality=50,
        force_format='WEBP',
        keep_meta=False
    )

    background_image = ResizedImageField(
        upload_to='background',
        verbose_name="Background Image",
        help_text=("The image displayed layered behind server buttons. This image will "
                    "cover the defined Secondary Color if used. Image will be resized to "
                    "1920x1080 after uploading."),
        blank=True,
        size=[1920,1080],
        quality=90,
        force_format='WEBP',
        keep_meta=False
    )
    
    avatar_image = ResizedImageField(
        upload_to='avatar',
        verbose_name="Avatar Image",
        help_text=("The image displayed in OpenGraph embeds, such as when a link is " 
                   "pasted to a Discord Channel or a Twitter post. This should be a 1x1 ratio image. "
                   "This will also be used as your Favicon, after being converted to a .ico file."),
        blank=True,
        size=[500,500],
        quality=100,
        force_format='WEBP',
        keep_meta=False
    )
    
    meta_description = models.CharField(
        max_length=500,
        verbose_name="Meta Description",
        help_text=("The description for your website provided in search engine results. "
                    "This will apply to all pages that do not override."),
        default="",
        blank=True
    )
    
    meta_keywords = models.CharField(
        max_length=500,
        verbose_name="Meta Keywords",
        help_text=("A series of comma-separated values that represent meta keywords used "
                    "in search engine results. This will apply to all pages that do not override."),
        default="",
        blank=True
    )
    
    use_main_color = models.BooleanField(
        verbose_name="Use Main Color",
        help_text=("If this is checked, the Main Color chosen above will be used on the website."),
        default=True
    )
    
    use_secondary_color = models.BooleanField(
        verbose_name="Use Secondary Color",
        help_text=("If this is checked, the Secondary Color chosen above will be used on the website. "
                   "If you are using a Background Image, that will always take precedence."),
        default=True
    )
    
    enable_footer = models.BooleanField(
        verbose_name="Enable Footer",
        help_text=("If this is checked, the footer will be enabled"),
        default=True
    )
    
    enable_footer_credit = models.BooleanField(
        verbose_name="Enable Credits in Footer",
        help_text=("If this is checked, a link to the raptor-web repository will appear in the footer. "),
        default=True
    )
    
    enable_footer_contact = models.BooleanField(
        verbose_name="Enable Email in Footer",
        help_text=("If this is checked, a mailto link will appear in the footer, "
                   "addressed to the defined contact email."),
        default=True
    )
    
    require_login_for_user_list = models.BooleanField(
        verbose_name="Require login to access Site Members",
        help_text=("If this is checked, users will need to create an account and, "
                   "log in before they can access the Site Members list."),
        default=True
    )
    
    enable_server_query = models.BooleanField(
        verbose_name="Enable server querying and player counts section",
        help_text=("If this is un-checked, the address/port of created Servers will NOT be, "
                   "queried for state and player data. Each server's information will still be "
                   "displayed on the website as normal, however the Player Counts section "
                   "of the Header Box will no longer appear, or the server status indicators."),
        default=True
    )
    
    collapse_network_rules_when_accessing_server_rules = models.BooleanField(
        verbose_name="Collapse Network Rules section if accessing Rules page from a Server modal link.",
        help_text=("If this is un-checked, the Network Rules section on the Rules page will NOT be "
                   "collapsed when accessing Rules from a Server Modal."),
        default=True
    )
    
    navigation_from_top = models.BooleanField(
        verbose_name="Navigation popup from top of screen.",
        help_text=("If this is checked, the Navigation popup will come from "
                   "the top of the screen rather than the left."),
        default=True
    )
    
    send_donation_email = models.BooleanField(
        verbose_name="Send emails upon successful donations.",
        help_text=("If this is checked, emails will be sent to donators "
                   "if they are logged into an account when donating."),
        default=True
    )
    
    donation_goal = models.IntegerField(
        verbose_name="Monthly Donation Goal.",
        help_text=("The monthly donation goal in USD. This will reset "
                   "at the beginning of every month."),
        validators=[
            MaxValueValidator(100000),
            MinValueValidator(1)
        ],
        default=1
    )
    
    show_donation_goal = models.BooleanField(
        verbose_name="Show Monthly Donation Goal.",
        help_text=("Whether the monthly donation goal will appear on the website"),
        default=True
    )
    
    server_pagination_count = models.IntegerField(
        verbose_name="Server buttons per-page",
        help_text=("How many server buttons will appear per page. If the amount of Servers exceeds "
                   "this amount, a set if Next and Previous buttons will appear to cycle between pages "
                   "of created servers."),
        validators=[
            MaxValueValidator(12),
            MinValueValidator(1)
        ],
        choices=[(i, i) for i in range(1, 13)],
        default=6
    )
    
    discord_guild = models.CharField(
        verbose_name="Discord Guild ID.",
        help_text=("Set this to the ID for the Discord Guild that the Bot will be linked to. "
                   "The bot will be able to read announcements and send server information messages here."),
        max_length=500,
        default="0"
    )
    
    discord_global_announcement_channel = models.CharField(
        verbose_name="Global Announcements Discord Channel ID",
        help_text=("Set this to the ID for the Discord Channel that the Bot will be looking for " 
                   "global announcements from."),
        max_length=500,
        default="0"
    )
    
    discord_staff_role = models.CharField(
        verbose_name="Discord Staff Role ID.",
        help_text=("Set this to the ID for the Discord Role that the Bot will read messages from as announcements. " 
                   "Discord Users without this role will not be able to create announcements. "),
        max_length=500,
        default="0"
    )

    def __str__(self):
        return str(self.brand_name)

    class Meta:
        verbose_name = "Site Settings",
        verbose_name_plural = "Site Settings"
        permissions = [
            ("panel", "Can access the Control Panel Homepage"),
            ("discord_bot", "Can access the Discord Bot control panel"),
            ("server_actions", "Can access the Server Actions menu"),
            ("reporting", "Can access Reporting"),
            ("donations", "Can access Donations"),
            ("settings", "Can access settings (DANGEROUS!)"),
        ]
        
        
class SmallSiteInformation(models.Model):
    """
    Extra site information. Hidden from the user.
    """
    ico_image = ResizedImageField(
        upload_to="ico",
        force_format="ICO",
        size=[64, 64],
        quality=5,
        blank=True
    )

    def __str__(self):
        return str(self.brand_name)

    class Meta:
        verbose_name = "Site Information",
        verbose_name_plural = "Site Information"
            

class InformativeText(models.Model):
    """
    A block of information which is placed at the header of most
    default pages. A page must be visited first for it's InformativeText
    to appear here.
    """
    enabled = models.BooleanField(
        default=True,
        verbose_name="Enabled"
    )

    name = models.CharField(
        max_length=50,
        default="Default",
        verbose_name="Content Name"
    )

    content = models.CharField(
        max_length=15000,
        default = "",
        verbose_name="Content"
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Informative Text",
        verbose_name_plural = "Informative Texts"
        
        
class DefaultPages(models.Model):
    """
    Enable or disable the default pages supplied with the website. If you uncheck a page here, it will
    not appear in the navigation sidebar, and attempts to manually access the URL will lead to the 404
    page.
    """
    announcements = models.BooleanField(
        default=True,
        verbose_name="Announcements Page",
        help_text="Whether the default Announcement page is enabled or not."
    )
    
    rules = models.BooleanField(
        default=True,
        verbose_name="Rules Page",
        help_text="Whether the default Rules page is enabled or not."
    )
    
    banned_items = models.BooleanField(
        default=True,
        verbose_name="Banned Items Page",
        help_text="Whether the default Banned Items page is enabled or not."
    )
    
    voting = models.BooleanField(
        default=True,
        verbose_name="Voting Page",
        help_text="Whether the default Vote for Us page is enabled or not."
    )
    
    joining = models.BooleanField(
        default=True,
        verbose_name="How to Join Page",
        help_text="Whether the default How to Join page is enabled or not."
    )
    
    staff_apps = models.BooleanField(
        default=True,
        verbose_name="Staff Applications Page",
        help_text="Whether the default Staff Applications page is enabled or not."
    )
    
    members = models.BooleanField(
        default=True,
        verbose_name="Site Members Page",
        help_text=("Whether the default Site Members list page is enabled or not. "
                   "This will also prevent non-admin users from accessing any "
                   "profiles except for their own.")
    )
    
    onboarding = models.BooleanField(
        default=True,
        verbose_name="Onboarding Pages",
        help_text=("Whether the default pages that contain all information "
                    "about each server are enabled or not.")
    )
    
    donations = models.BooleanField(
        default=True,
        verbose_name="Donations Pages",
        help_text=("Whether the Donations system/pages are enabled or not.")
    )

    def __str__(self):
        return "Default Pages"

    class Meta:
        verbose_name = "Default Pages",
        verbose_name_plural = "Default Pages"


@receiver(post_save, sender=SiteInformation)
def post_save_site_info(sender, instance, *args, **kwargs):
    """
    If a new Avatar is added to SiteInformation, convert that image 
    to a .ICO format and save it to SmallSiteInformation's ico_image
    attribute.
    
    This runs every time SiteInformation model is saved. The function
    checks to see if the current Avatar Image hash is different than 
    the .ico filename, which is set to the Avatar Image hash on
    creation. It will only run if those two values differ.
    """
    small_site_info: SmallSiteInformation.objects = SmallSiteInformation.objects.get_or_create(pk=1)[0]
    
    if instance.avatar_image:
        if f"ico/{hash(instance.avatar_image)}.ico" != f"{small_site_info.ico_image}":
            small_site_info.ico_image.save(
                f"{hash(instance.avatar_image)}.ico",
                instance.avatar_image)
            small_site_info.save()
            LOGGER.info("New Avatar Image detected, new favicon created from it.")
            
@receiver(pre_save, sender=NotificationToast)
def strip_script_tags(sender, instance, *args, **kwargs):
    """
    Before saving a Toast's message, remove any html script tags from the message.
    """
    cleaned_message = sub(r'<.*/script.*?>', '', instance.message)
    instance.message = cleaned_message
