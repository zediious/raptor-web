from django import forms
import logging

LOGGER = logging.Logger("form_validator_logger")

class AdminApp(forms.Form):

    name = forms.CharField()
    email = forms.EmailField()
    whether_developer = forms.BooleanField(label="Do you have a background in Software Development, particularly back-end?")
    why_join = forms.CharField(widget=forms.Textarea)
    botTrapA = forms.CharField(required=False, widget=forms.HiddenInput)

    def clean_botTrapA(self):

        botTrapA = self.cleaned_data['botTrapA']

        if len(botTrapA) > 0:

            LOGGER.error("[WARN] Hidden input field was filled out in AdminApp, likely a BOT.")
            raise forms.ValidationError("")

class ModApp(forms.Form):

    name = forms.CharField()
    email = forms.EmailField()
    why_join = forms.CharField(widget=forms.Textarea)
    botTrapM = forms.CharField(required=False, widget=forms.HiddenInput)

    def clean_botTrapM(self):

        botTrapM = self.cleaned_data['botTrapM']

        if len(botTrapM) > 0:

            LOGGER.error("[WARN] Hidden input field was filled out in ModApp, likely a BOT.")
            raise forms.ValidationError("")
