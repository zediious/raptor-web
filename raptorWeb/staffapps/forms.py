from django import forms
from django.core import validators
import logging

from staffapps.models import ModeratorApplication, AdminApplication

LOGGER = logging.Logger("form_validator_logger")

FORM_LABELS = {
    "ask_age": "How old are you?",
    "age_admin": "You must be at least 18 years old to apply directly for admin",
    "age_mod": "You must be at least 10 years old to apply",
    "time_commitment": "What Timezone do you live in? How often and at what time of the day will you be available?",
    "mc_name": "What is your Minecraft In-Game name?",
    "discord_help": "Format it as such: Zediious#1234",
    "mc_name_verify": "Confirm your Minecraft In-Game name.",
    "discord_name": "What is your Discord Username?",
    "discord_name_verify": "Confirm your Discord Username",
    "voice_chat": "Do you have a working microphone and are comfortable speaking in Voice Chat?",
    "description": "Give a general description of yourself, and how you operate.",
    "contact_uppers": "Do you have the ability to quickly establish the problem, and get in contact with higher up if someone is breaking the rules and/or hacking?",
    "plugin_help": "Our 1.16.5 servers use server-side mods rather than plugins.",
    "server_api": "Are you familiar with/have used Minecraft reverse proxy software as well as the various APIs to integrate Forge with plugins (SpongeForge, Mohist, Magma)?",
    "it_knowledge": "How much knowledge to do you have in terms of IT/networking/software development? If your profession includes either of these skills that is very useful information.",
    "it_help": "Having a basic understanding of network concepts is the bare minimum.",
    "linux": "How much experience and/or knowledge do you have regarding Linux system administration and general usage?",
    "ptero": "Are you familiar with the Pterodactyl Game Server management panel and its usage?",
    "ptero_help": "Having set up /configuring an instance of Pterodactyl yourself is not a requirement.",
    "experience_help": "Any Admin roles you've had outside of Minecraft may also be described here.",
    "why_join": "Why do you want to join the ShadowRaptor staff team?",
    "experience": "Please provide as much information as you can about any Admin roles you've had on Minecraft servers, whether you owned the server or were staff. \
        Describe what exactly it was you did for the server you were staff of in as much detail as possible.",
    "modpack_knowledge": "Administrating a modded server requires good knowledge of how mods play, to properly identify certain things. \
        Have you played the modpacks we run on our network, \and/or have a good understanding of how they/modded Minecraft in general works? \
            Provide a short history of your time with Minecraft here as well.",
    "plugin_knowledge": "Plugin/server-side mod knowledge is a necessity to become an Admin. Are there are any plugins in particular that you \
        have extensive experience with? Do you believe that you can adapt to different configurations?",
}

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

def verify_minecraft_username(clean_data):
        """
        Common function for staff application clean() methods to verify Minecraft username
        """
        minecraft = clean_data.get("mc_name")
        v_minecraft = clean_data.get("verify_mc")
        
        if not(minecraft == v_minecraft):
            raise forms.ValidationError("Minecraft username fields must match")

def verify_discord_username(clean_data):
        """
        Common function for staff application clean() methods to verify Discord username
        """
        discord = clean_data.get("discord_name")
        v_discord = clean_data.get("verify_discord")
        
        if not(discord == v_discord):
            raise forms.ValidationError("Discord username fields must match")

class StaffAppForm(forms.ModelForm):
    """
    ModelForm for an Admin Application
    """
    time = forms.CharField(
        label=FORM_LABELS["time_commitment"], 
        max_length=150)

    mc_name = forms.CharField(
        label=FORM_LABELS["mc_name"], 
        max_length=50)

    verify_mc = forms.CharField(
        label=FORM_LABELS["mc_name_verify"], 
        max_length=50)

    discord_name = forms.CharField(
        label=FORM_LABELS["discord_name"], 
        help_text=FORM_LABELS["discord_help"], max_length=50, validators=[check_for_hash])

    verify_discord = forms.CharField(
        label=FORM_LABELS["discord_name_verify"], 
        max_length=50, validators=[check_for_hash])

    voice_chat = forms.BooleanField(
        label=FORM_LABELS["voice_chat"], 
        required=False)

    description = forms.CharField(
        label=FORM_LABELS["description"], 
        max_length=500, widget=forms.Textarea)

    modpacks = forms.CharField(
        label=FORM_LABELS["modpack_knowledge"], 
        max_length=300, widget=forms.Textarea)

    experience = forms.CharField(
        label=FORM_LABELS["experience"], 
        help_text=FORM_LABELS["experience_help"], max_length=500, widget=forms.Textarea)

    why_join = forms.CharField(
        label=FORM_LABELS["why_join"],
        max_length=500, widget=forms.Textarea)

    trap = forms.CharField(
        required=False, 
        widget=forms.HiddenInput, validators=[validators.MaxLengthValidator(0)])

    def clean(self):
        """
        Overrides default clean, while calling the superclass clean()
        """
        cleaned_data = super().clean()
        verify_minecraft_username(cleaned_data)
        verify_discord_username(cleaned_data)

class AdminApp(StaffAppForm):
    """
    ModelForm for an Admin Application
    """
    age = forms.IntegerField(
        label=FORM_LABELS["ask_age"], 
        help_text=FORM_LABELS["age_admin"], max_value=99 , validators=[validate_admin_age])
    
    plugins = forms.CharField(
        label=FORM_LABELS["plugin_knowledge"], 
        help_text=FORM_LABELS["plugin_help"], max_length=300, widget=forms.Textarea)

    api = forms.CharField(
        label=FORM_LABELS["server_api"], 
        max_length=150, widget=forms.Textarea)

    it_knowledge = forms.CharField(
        label=FORM_LABELS["it_knowledge"], 
        help_text=FORM_LABELS["it_help"], max_length=300, widget=forms.Textarea)

    linux = forms.CharField(
        label=FORM_LABELS["linux"], 
        max_length=200, widget=forms.Textarea)

    ptero = forms.CharField(
        label=FORM_LABELS["ptero"], 
        max_length=150, help_text=FORM_LABELS["ptero_help"], widget=forms.Textarea)

    class Meta:
        model = AdminApplication
        exclude = ['verify_mc', 'verify_discord', 'trap']

class ModApp(StaffAppForm):
    """
    ModelForm for a Moderator Application
    """
    age = forms.IntegerField(
        label=FORM_LABELS["ask_age"], 
        help_text=FORM_LABELS["age_mod"], max_value=99 , validators=[validate_age])
    
    contact_uppers = forms.CharField(
        label=FORM_LABELS["contact_uppers"], 
        max_length=100)

    class Meta:
        model = ModeratorApplication
        exclude = ['verify_mc', 'verify_discord', 'trap']
