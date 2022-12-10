from django import forms
from django.core import validators
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import logging

from raptormc.models import AdminApplication, ModeratorApplication, User, UserProfileInfo, DiscordUserInfo

LOGGER = logging.Logger("form_validator_logger")

def check_for_hash(value):
    """
    Ensure Discord name value contains a '#' symbol
    """
    if value.find("#") < 0:

        raise forms.ValidationError("Format your Discord Username as indicated in the help text.")

def validate_age(value):
    """
    Ensure age value is at least 10
    """
    if value < 10:

        raise forms.ValidationError("You must be at least ten years old to apply for staff")

def validate_admin_age(value):
    """
    Ensure age value is at least 18
    """
    if value < 18:

        raise forms.ValidationError("You must be at least 18 years old to apply directly for Admin. One can still be promoted from a lower rank.")

class AdminApp(forms.ModelForm):
    """
    ModelForm for an Admin Application
    """
    position = forms.CharField(
        required=True, widget=forms.HiddenInput, initial="Admin")

    age = forms.IntegerField(
        label="How old are you?", 
        help_text="You must be at least 18 years old to apply directly for admin", max_value=99 , validators=[validate_admin_age])

    time = forms.CharField(
        label="What Timezone do you live in? How often and at what time of the day will you be available?", 
        max_length=150)

    mc_name = forms.CharField(
        label="What is your Minecraft In-Game name?", 
        max_length=50)

    verify_mc = forms.CharField(
        label="Confirm your Minecraft In-Game name.", 
        max_length=50)

    discord_name = forms.CharField(
        label="What is your Discord Username?", 
        help_text="Format it as such: Zediious#1234", max_length=50, validators=[check_for_hash])

    verify_discord = forms.CharField(
        label="Confirm your Discord username.", 
        max_length=50, validators=[check_for_hash])

    voice_chat = forms.BooleanField(
        label="Do you have a working microphone and are comfortable speaking in Voice Chat?", 
        required=False)

    description = forms.CharField(
        label="Give a general description of yourself, and how you operate.", 
        max_length=500, widget=forms.Textarea)

    modpacks = forms.CharField(
        label="Administrating a modded server requires good knowledge of how mods play, to properly identify certain things. Have you played the modpacks we run on our network, and/or have a good understanding of how they/modded Minecraft in general works? Provide a short history of your time with Minecraft here as well.", 
        max_length=300, widget=forms.Textarea)

    plugins = forms.CharField(
        label="Plugin/server-side mod knowledge is a necessity to become an Admin. Are there are any plugins in particular that you have extensive experience with? Do you believe that you can adapt to different configurations?", 
        help_text="Our 1.16.5 servers use server-side mods rather than plugins.", max_length=300, widget=forms.Textarea)

    api = forms.CharField(
        label="Are you familiar with/have used Minecraft reverse proxy software as well as the various APIs to integrate Forge with plugins (SpongeForge, Mohist, Magma)?", 
        max_length=150, widget=forms.Textarea)

    IT_knowledge = forms.CharField(
        label="How much knowledge to do you have in terms of IT/networking/software development? If your profession includes either of these skills that is very useful information.", 
        help_text="Having a basic understanding of network concepts is the bare minimum.", max_length=300, widget=forms.Textarea)

    linux = forms.CharField(
        label="How much experience and/or knowledge do you have regarding Linux system administration and general usage?", 
        max_length=200, widget=forms.Textarea)

    ptero = forms.CharField(
        label="Are you familiar with the Pterodactyl Game Server management panel and its usage?", 
        max_length=150, help_text="Having set up /configuring an instance of Pterodactyl yourself is not a requirement.", widget=forms.Textarea)

    experience = forms.CharField(
        label="Please provide as much information as you can about any Admin roles you've had on Minecraft servers, whether you owned the server or were staff. Describe what exactly it was you did for the server you were staff of in as much detail as possible. ", 
        help_text="Any Admin roles you've had outside of Minecraft may also be described here.", max_length=500, widget=forms.Textarea)

    why_join = forms.CharField(
        label="Why do you want to join the ShadowRaptor staff team?",
        max_length=500, widget=forms.Textarea)

    trap = forms.CharField(
        required=False, 
        widget=forms.HiddenInput, validators=[validators.MaxLengthValidator(0)])

    class Meta:
        model = AdminApplication
        exclude = ['verify_mc', 'verify_discord', 'trap']

    def clean(self):
        """
        Overrides default clean, while calling the superclass clean()
        Ensures MC and Discord names are the same in validation fields.
        """
        clean_data = super().clean()
        discord = clean_data.get("discord_name")
        v_discord = clean_data.get("verify_discord")
        minecraft = clean_data.get("mc_name")
        v_minecraft = clean_data.get("verify_mc")

        if not(minecraft == v_minecraft):
            raise forms.ValidationError("Minecraft username fields must match")
        
        if not(discord == v_discord):
            raise forms.ValidationError("Discord username fields must match.")

class ModApp(forms.ModelForm):
    """
    ModelForm for a Moderator Application
    """
    position = forms.CharField(
        required=True, 
        widget=forms.HiddenInput, initial="Mod")

    age = forms.IntegerField(
        label="How old are you?", 
        help_text="You must be at least 10 years old to apply", max_value=99 , validators=[validate_age])

    time = forms.CharField(
        label="What Timezone do you live in? How often and at what time of the day will you be available?", 
        max_length=150)

    mc_name = forms.CharField(
        label="What is your Minecraft In-Game name?", 
        max_length=50)

    verify_mc = forms.CharField(
        label="Confirm your Minecraft In-Game name.", 
        max_length=50)

    discord_name = forms.CharField(
        label="What is your Discord Username?", 
        help_text="Format it as such: Zediious#1234", max_length=50, validators=[check_for_hash])

    verify_discord = forms.CharField(
        label="Confirm your Discord username.", 
        max_length=50, validators=[check_for_hash])

    voice_chat = forms.BooleanField(
        label="Do you have a working microphone and/or are comfortable speaking in Voice Chat?", 
        required=False)

    contact_uppers = forms.CharField(
        label="Do you have the ability to quickly establish the problem, and get in contact with higher up if someone is breaking the rules and/or hacking?", 
        max_length=100)

    description = forms.CharField(
        label="Give a general description of yourself, and how you operate.", 
        max_length=500, widget=forms.Textarea)

    modpacks = forms.CharField(
        label="Moderating a modded server requires good knowledge of how mods play, to properly identify certain things. Have you played the modpacks we run on our network, and/or have a good understanding of how they/modded Minecraft in general works? Provide a short history of your time with Minecraft.", 
        max_length=300, widget=forms.Textarea)

    experience = forms.CharField(
        label="Do you have any experience moderating a server/community? If so, please provide as much information as you can about each server, and your role in it.", 
        help_text="This is not limited to just Minecraft servers. If you have been on a moderation role on discord/other game servers, you may include that.", 
        max_length=500, widget=forms.Textarea)

    why_join = forms.CharField(
        label="Why do you want to join the ShadowRaptor staff team?", 
        max_length=500, widget=forms.Textarea)

    trap = forms.CharField(
        required=False, 
        widget=forms.HiddenInput, validators=[validators.MaxLengthValidator(0)])

    class Meta:
        model = ModeratorApplication
        exclude = ['verify_mc', 'verify_discord', 'trap']
    
    def clean(self):
        """
        Overrides default clean, while calling the superclass clean()
        Ensures MC and Discord names are the same in validation fields.
        """
        clean_data = super().clean()
        discord = clean_data.get("discord_name")
        v_discord = clean_data.get("verify_discord")
        minecraft = clean_data.get("mc_name")
        v_minecraft = clean_data.get("verify_mc")

        if not(minecraft == v_minecraft):
            raise forms.ValidationError("Minecraft username fields must match")

        if not(discord == v_discord):
            raise forms.ValidationError("Discord username fields must match.")

class UserForm(forms.ModelForm):
    """
    Standard information in User Registration form
    """
    password = forms.CharField(widget=forms.PasswordInput())
    password_v = forms.CharField(label="Verify Password", widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'email', 'password')

    def clean(self):
        """
        Overrides default clean, while calling the superclass clean()
        Ensures password fields are the same.
        """
        clean_data = super().clean()
        password = clean_data.get("password")
        v_password = clean_data.get("password_v")

        if not(password == v_password):

            raise forms.ValidationError("Password fields must match")

class UserProfileInfoForm(forms.ModelForm):
    """
    Extra information in User Registration form
    """  
    class Meta():
        model = UserProfileInfo
        fields = ('profile_picture', 'minecraft_username', 'favorite_modpack')

class DiscordUserInfoForm(forms.ModelForm):
    """
    Information from a Discord User that can be changed
    """ 
    class Meta():
        model = DiscordUserInfo
        fields = ('minecraft_username', 'favorite_modpack')

class UserLoginForm(forms.Form):
    """
    User Login form
    """
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        """
        Overrides default clean, while calling the superclass clean()
        Ensures a User exists and that password is correct before 
        returning clean data to view
        """
        clean_data = super().clean()
        username = clean_data.get("username")
        password = clean_data.get("password")
        user_exists = False
        for user in User.objects.all():
            if user.username == username:
                user_exists = True
                break

        if user_exists == False:
            raise forms.ValidationError("The entered Username does not exist")

        if authenticate(username=username, password=password) == None:
            raise forms.ValidationError("The entered Password was incorrect")