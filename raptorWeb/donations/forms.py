from django import forms

class SubmittedDonationForm(forms.Form):
    minecraft_username = forms.CharField(
        required=True,
    )
