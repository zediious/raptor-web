from django.db import models


class NotificationToast(models.Model):
    """
    Represents a website notification toast
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


class NavbarDropdown(models.Model):
    """
    Represents a dropdown menu for the Navigation bar
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
    Represents an added Navigation link
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
        default="/"
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

    class Meta:
        verbose_name = "Navigation Link",
        verbose_name_plural = "Navigation Links"


class SiteInformation(models.Model):
    """
    Represents site information such as branding images, colors, etc
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

    def __str__(self):
        return str(self.brand_name)

    class Meta:
        verbose_name = "Site Information",
        verbose_name_plural = "Site Information"


class InformativeText(models.Model):
    """
    Represents a general block of information 
    which is placed in the website.
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
