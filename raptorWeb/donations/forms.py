from django import forms

class SubmittedDonationForm(forms.Form):
    minecraft_username = forms.CharField(
        required=True,
    )
    
    discord_username = forms.CharField(
        help_text=("This is not required, but you must enter a Discord "
                   "username if you want to receive Roles on Discord."),
        required=False,
    )
    
    
class DonationDiscordUsernameForm(forms.Form):
    discord_username = forms.CharField(
        help_text=("This is not required, but you must enter a Discord "
                   "username if you want to receive Roles on Discord."),
        required=False,
    )
    
    
class DonationPriceForm(forms.Form):
    chosen_price = forms.IntegerField(
        help_text=("Enter any whole amount you would like to donate "
                   "above the package's price."),
        required=False
    )
