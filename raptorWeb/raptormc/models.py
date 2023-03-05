from django.db import models
from django.utils.text import slugify


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

    nav_image = models.ImageField(
        upload_to='navwidgetimage',
        verbose_name="Nav Widget Image",
        help_text=("The image used as an identifier/name for this Nav Widget. "
                    "Optimal size for this image is w250xh72 or within the same aspect ratio."),
        blank=True
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
    Website information such as Brand Name, images, colors, and more.
    """
    brand_name = models.CharField(
        max_length=100,
        verbose_name="Website/Network Name",
        help_text=("The name of your website and/or network"),
        default="Default"
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
                    "underneath server buttons"),
        default="#00233c"
    )

    branding_image = models.ImageField(
        upload_to='branding',
        verbose_name="Branding Image",
        help_text=("The image displayed in the website Navigation Bar as a link to the "
                    "homepage. Optimal size for this image is w800xh200."),
        blank=True
    )

    background_image = models.ImageField(
        upload_to='background',
        verbose_name="Background Image",
        help_text=("The image displayed layered behind server buttons. This image will "
                    "cover the defined Secondary Color if used. Optimal size for this image "
                    " is 1920x1080 or within the same aspect ratio."),
        blank=True
    )
    
    meta_description = models.CharField(
        max_length=500,
        verbose_name="SEO - Meta Description",
        help_text=("The description for your website provided in search engine results. "
                    "This will apply to all pages that do not override."),
        default="",
        blank=True
    )
    
    meta_keywords = models.CharField(
        max_length=500,
        verbose_name="SEO - Meta Keywords",
        help_text=("A series of comma-separated values that represent meta keywords used "
                    "in search engine results. This will apply to all pages that do not override."),
        default="",
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
