from django.utils.translation import gettext_lazy as _

from django.db import models
        

class StaffApplication(models.Model):
    """
    This model is depracated
    """
    class ApplicationStatusChoices(models.TextChoices):
        APPROVED = 'A', _('Approved')
        DENIED = 'D', _('Denied')
        PENDING = 'P', _('Pending')

    approved = models.CharField(
        max_length=1,
        choices=ApplicationStatusChoices.choices,
        default=ApplicationStatusChoices.PENDING
    )

    age = models.IntegerField(
        verbose_name="Applicant age",
        default="Default")

    time = models.CharField(
        max_length=500, 
        verbose_name="Time Zone and alottable time",
        default="Default")

    mc_name = models.CharField(
        max_length=500, 
        verbose_name="Minecraft Username",
        default="Default")

    discord_name = models.CharField(
        max_length=500, 
        verbose_name="Discord Username/ID",
        default="Default")

    voice_chat = models.BooleanField(
        max_length=500,
        default=False,
        verbose_name="Capable of using Voice Chat?")

    description = models.TextField(
        max_length=500, 
        verbose_name="General self-description",
        default="Default")

    modpacks = models.TextField(
        max_length=500, 
        verbose_name="Knowledge of server modpacks/general Modded Minecraft",
        default="Default")

    experience = models.TextField(
        max_length=500, 
        verbose_name="Experience on other servers",
        default="Default")

    why_join = models.TextField(
        max_length=500, 
        verbose_name="Reasons for wanting to be staff.",
        default="Default")

    def __str__(self):
        return str(
            "Application from: {}".format(self.discord_name)
            )

    class Meta:
        abstract = True

class AdminApplication(StaffApplication):
    """
    This model is depracated
    """
    position = models.CharField(
        max_length=100,
        default="Admin",
        editable=False
    )
    
    plugins = models.TextField(
        max_length=500, 
        verbose_name="Knowledge of plugins/server mods and adaptability",
        default="Default")

    api = models.TextField(
        max_length=500, 
        verbose_name="Knowledge of server APIs and Minecraft proxies.",
        default="Default")

    it_knowledge = models.TextField(
        max_length=500, 
        verbose_name="IT/Software/Networking knowledge, as well as whether one's work involves these topics.",
        default="Default")

    linux = models.TextField(
        max_length=500, 
        verbose_name="Knowledge in Linux System Administration and CLI use.",
        default="Default")

    ptero = models.TextField(
        max_length=500, 
        verbose_name="Knowledge of Pterodactyl Panel",
        default="Default")

    class Meta:
        verbose_name = 'Admin Application'
        verbose_name_plural = 'Admin Applications'

class ModeratorApplication(StaffApplication):
    """
    This model is depracated
    """

    position = models.CharField(
        max_length=100,
        default="Mod",
        editable=False
    )
    
    contact_uppers = models.TextField(
        max_length=500, 
        verbose_name="Ability to reach higher-ups",
        default="Default")

    class Meta:
        verbose_name = 'Moderator Application'
        verbose_name_plural = 'Moderator Applications'
        
        
class StaffApplicationField(models.Model):
    """
    A created field to be put into a form
    """
    
    class StaffApplicationFieldWidgetChoices(models.TextChoices):
        TEXT = 'text', _('Text'),
        INT = 'int', _('Number')
        BOOL = 'bool', _('Yes or No')
        
    name = models.CharField(
        max_length=500,
        verbose_name='Field Name',
        help_text='The name of this field'
    )
    
    help_text = models.CharField(
        max_length=500,
        verbose_name='Help Text',
        help_text='The help text of this field'
    )
    
    widget = models.CharField(
        max_length=5,
        verbose_name='Form Widget',
        help_text='The widget type used for this form',
        choices=StaffApplicationFieldWidgetChoices.choices,
        default=StaffApplicationFieldWidgetChoices.TEXT
    )
    
    priority = models.IntegerField(
        default=0,
        verbose_name='Priority',
        help_text='The order that this field will appear in forms it is added to.'
    )
    
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = 'Form Field'
        verbose_name_plural = 'Form Fields'
    
    
class CreatedStaffApplication(models.Model):
    """
    A created Staff Application to be submitted by users. Create Form Fields and attach
    them to the created Staff Application to customize the form.
    """
    
    name = models.CharField(
        max_length=500,
        verbose_name='Staff Application Name',
        help_text='The name of this Staff Application and/or the position being applied for',
        default="Default"
    )
    
    form_fields = models.ManyToManyField(
        to=StaffApplicationField,
        blank=False,
        verbose_name="Form Fields",
        help_text="A list of created Form Fields that will be used in this Staff Application."
    )
    
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = 'Created Staff Application'
        verbose_name_plural = 'Created Staff Applications'
    
    
class SubmittedStaffApplication(models.Model):
    """
    A Staff Application that has been submitted by a user.
    """
    
    class ApplicationStatusChoices(models.TextChoices):
        APPROVED = 'A', _('Approved')
        DENIED = 'D', _('Denied')
        PENDING = 'P', _('Pending')
    
    submitted_data = models.JSONField(
        default=dict,
        help_text="JSON data representing the submitted form fields",
        verbose_name="Submitted Data",
        blank=True,
        null=True
    )
    
    submitted_date = models.DateTimeField(
        verbose_name="Originally Sent",
        auto_now_add=True
    )

    approved = models.CharField(
        max_length=1,
        choices=ApplicationStatusChoices.choices,
        default=ApplicationStatusChoices.PENDING
    )
    
    def __str__(self) -> str:
        return f'Submitted: {self.submitted_date.strftime("%B %d %Y")} at {self.submitted_date.strftime("%H:%M")}'
    
    class Meta:
        permissions = [
            ("approval_submittedstaffapplication", "Can approve or deny Submitted Staff Applications"),
        ]
        verbose_name = 'Submitted Staff Application'
        verbose_name_plural = 'Submitted Staff Applications'
