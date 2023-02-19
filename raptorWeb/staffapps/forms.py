import logging
from typing import Any

from django import forms
from django.core import validators

from captcha.fields import CaptchaField

from raptorWeb.staffapps.models import ModeratorApplication, AdminApplication
from raptorWeb.staffapps.util import form_labels

LOGGER = logging.Logger("form_validator_logger")

def check_for_hash(value: str) -> None:
    """
    Ensure Discord name value contains a '#' symbol
    """
    if value.find("#") < 0:

        raise forms.ValidationError("Format your Discord Username as indicated in the help text.")

def validate_age(value: int) -> None:
    """
    Ensure age value is at least 10
    """
    if value < 10:

        raise forms.ValidationError("You must be at least ten years old to apply for staff")

def validate_admin_age(value: int) -> None:
    """
    Ensure age value is at least 18
    """
    if value < 18:

        raise forms.ValidationError("You must be at least 18 years old to apply directly for Admin. One can still be promoted from a lower rank.")

def verify_minecraft_username(clean_data: dict[str, Any]) -> None:
        """
        Common function for staff application clean() methods to verify Minecraft username
        """
        minecraft: str = clean_data.get("mc_name")
        v_minecraft: str = clean_data.get("verify_mc")
        
        if not(minecraft == v_minecraft):
            raise forms.ValidationError("Minecraft username fields must match")

def verify_discord_username(clean_data: dict[str, Any]) -> None:
        """
        Common function for staff application clean() methods to verify Discord username
        """
        discord: str = clean_data.get("discord_name")
        v_discord: str = clean_data.get("verify_discord")
        
        if not(discord == v_discord):
            raise forms.ValidationError("Discord username fields must match")

class StaffAppForm(forms.ModelForm):
    """
    ModelForm for an Admin Application
    """
    time = forms.CharField(
        label=form_labels.time_commitment, 
        max_length=150)

    mc_name = forms.CharField(
        label=form_labels.mc_name, 
        max_length=50)

    verify_mc = forms.CharField(
        label=form_labels.mc_name_verify, 
        max_length=50)

    discord_name = forms.CharField(
        label=form_labels.discord_name, 
        help_text=form_labels.discord_help, max_length=50, validators=[check_for_hash])

    verify_discord = forms.CharField(
        label=form_labels.discord_name_verify, 
        max_length=50, validators=[check_for_hash])

    voice_chat = forms.BooleanField(
        label=form_labels.voice_chat, 
        required=False)

    description = forms.CharField(
        label=form_labels.description, 
        max_length=500, widget=forms.Textarea)

    modpacks = forms.CharField(
        label=form_labels.modpack_knowledge, 
        max_length=300, widget=forms.Textarea)

    experience = forms.CharField(
        label=form_labels.experience, 
        help_text=form_labels.experience_help, max_length=500, widget=forms.Textarea)

    why_join = forms.CharField(
        label=form_labels.why_join,
        max_length=500, widget=forms.Textarea)

    captcha = CaptchaField()

    trap = forms.CharField(
        required=False, 
        widget=forms.HiddenInput, validators=[validators.MaxLengthValidator(0)])

    def clean(self):
        """
        Overrides default clean, while calling the superclass clean()
        """
        cleaned_data: dict[str, Any] = super().clean()
        verify_minecraft_username(cleaned_data)
        verify_discord_username(cleaned_data)

class AdminApp(StaffAppForm):
    """
    ModelForm for an Admin Application
    """
    age = forms.IntegerField(
        label=form_labels.ask_age, 
        help_text=form_labels.age_admin, max_value=99 , validators=[validate_admin_age])
    
    plugins = forms.CharField(
        label=form_labels.plugin_knowledge, 
        help_text=form_labels.plugin_help, max_length=300, widget=forms.Textarea)

    api = forms.CharField(
        label=form_labels.server_api, 
        max_length=150, widget=forms.Textarea)

    it_knowledge = forms.CharField(
        label=form_labels.it_knowledge, 
        help_text=form_labels.it_help, max_length=300, widget=forms.Textarea)

    linux = forms.CharField(
        label=form_labels.linux, 
        max_length=200, widget=forms.Textarea)

    ptero = forms.CharField(
        label=form_labels.ptero, 
        max_length=150, help_text=form_labels.ptero_help, widget=forms.Textarea)

    class Meta:
        model = AdminApplication
        exclude = ['verify_mc', 'verify_discord', 'trap', 'approved']

class ModApp(StaffAppForm):
    """
    ModelForm for a Moderator Application
    """
    age = forms.IntegerField(
        label=form_labels.ask_age, 
        help_text=form_labels.age_mod, max_value=99 , validators=[validate_age])
    
    contact_uppers = forms.CharField(
        label=form_labels.contact_uppers, 
        max_length=100)

    class Meta:
        model = ModeratorApplication
        exclude = ['verify_mc', 'verify_discord', 'trap', 'approved']
