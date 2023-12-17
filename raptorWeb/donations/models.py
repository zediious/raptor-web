from logging import Logger, getLogger

from django.db import models
from django.core.validators import MinValueValidator

from rcon.source import Client
from django_resized import ResizedImageField

from raptorWeb.gameservers.models import Server
from raptorWeb.authprofiles.models import RaptorUser

LOGGER: Logger = getLogger('donations.models')


class DonationServerCommand(models.Model):
    """
    A command to be sent to a server
    """
    command = models.CharField(
        default="",
        max_length=2000
    )
    
    def __str__(self) -> str:
        return f'`{self.command}`'

    class Meta:
        verbose_name = "Server Command"
        verbose_name_plural = "Server Commands"


class DonationPackage(models.Model):
    """
    A donation package
    """
    name = models.CharField(
        default="",
        max_length=150
    )
    
    package_description = models.CharField(
        max_length=1500,
        verbose_name="Package Description",
        help_text="A description of this donation package, along with the benefits it will give.",
        default="Package Description")
    
    package_picture = ResizedImageField(
        upload_to='package_pictures',
        verbose_name="Package Image",
        help_text=("An image associated with this donation package that will be displayed on the website. "
                    "This image will be resized to 250x250 after upload."),
        blank=True,
        size=[250,250],
        quality=80,
        force_format='WEBP',
        keep_meta=False)
    
    price = models.IntegerField(
        default=0,
        validators=[MinValueValidator(1)],
        verbose_name='Price',
        help_text='The price of this Package.'
    )
    
    variable_price = models.BooleanField(
        default=False,
        verbose_name='Variable Price',
        help_text='If this is enabled, users will be able to input any amount they wish to donate above 1 USD.'
    )
    
    allow_repeat = models.BooleanField(
        default=False,
        verbose_name='Allow multiple purchases',
        help_text='If this is enabled, this package can be bought multiple times by the same Minecraft username'
    )
    
    servers = models.ManyToManyField(
        to=Server,
        blank=True,
        verbose_name="Servers to send Commands to.",
        help_text="The servers that this package will send commands to."
    )

    commands = models.ManyToManyField(
        to=DonationServerCommand,
        blank=True,
        verbose_name="Commands to Send.",
        help_text="A list of created Server Commands to send when this package is bought."
    )
    
    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Donation Package"
        verbose_name_plural = "Donation Packages"
        
        
class CompletedDonation(models.Model):
    """
    A completed donation
    """
    donation_datetime = models.DateTimeField(
        verbose_name="Date and time of Donation",
        auto_now_add=True)
    
    donating_user = models.ForeignKey(
        to=RaptorUser,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Donating User",
        help_text=("The user who donated. This will be blank if the donator "
                   "was not logged in at the time of donation.")
    )
    
    minecraft_username = models.CharField(
        max_length=100,
        verbose_name="Minecraft Username of Donor",
        help_text=("The Minecraft username of the donating user. This will match the Minecraft "
                   "username of the associated user, if one exists.")
    )
    
    discord_username = models.CharField(
        blank=True,
        null=True,
        max_length=100,
        verbose_name="Discord tag of Donor",
        help_text=("The Discord tag of the donating user. This will match the Discord "
                   "tag of the associated user, if one exists.")
    )
    
    bought_package = models.ForeignKey(
        to=DonationPackage,
        verbose_name="Bought Package",
        on_delete=models.PROTECT,
        help_text="The package that was bought."
    )
    
    spent = models.IntegerField(
        default=0,
        verbose_name='Amount Spent',
        help_text='The amount spent for this donation.'
    )
    
    session_id = models.CharField(
        default="",
        max_length=1000,
        verbose_name="Session ID",
        help_text=("The session ID used when this donation took place")
    )
    
    checkout_id = models.CharField(
        default="",
        max_length=1000,
        verbose_name="Stripe Checkout ID",
        help_text=("The unique ID for the Stripe Checkout session this Donation utilized.")
    )
    
    sent_commands_count = models.IntegerField(
        default=0,
        verbose_name="Times commands were sent",
        help_text="The amount of times commands were sent for this donation."
    )
    
    completed = models.BooleanField(
        default=False,
        verbose_name="Completed",
        help_text="Whether this donation has been finalized and paid for."
    )
    
    def __str__(self) -> str:
        return f'Donation from {self.minecraft_username} for {self.bought_package}'
    
    def send_server_commands(self):
        """
        Send commands to servers
        """
        
        for server in self.bought_package.servers.all():
            with Client(
                server.rcon_address,
                server.rcon_port,
                passwd=server.rcon_password) as client:
                
                for command in self.bought_package.commands.all():
                    response = client.run(command.command)
                    LOGGER.debug(response)
                    
        self.sent_commands_count += 1
        self.save()
    