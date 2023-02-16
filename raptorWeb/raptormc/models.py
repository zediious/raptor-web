from django.db import models


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
