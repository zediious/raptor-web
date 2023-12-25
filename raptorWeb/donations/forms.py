from django import forms

class SubmittedDonationForm(forms.Form):
    minecraft_username = forms.CharField(
        label='Minecraft Username',
        help_text=("Your Minecraft in-game name. This must be supplied, and "
                   "and it must be a real Minecraft username."),
        required=True,
    )
    
    discord_username = forms.CharField(
        label='Discord Username',
        help_text=("This is not required, but you must enter a Discord "
                   "username if you want to receive Roles on Discord."),
        required=False,
    )
    
    
class DonationDiscordUsernameForm(forms.Form):
    discord_username = forms.CharField(
        label='Discord Username',
        help_text=("This is not required, but you must enter a Discord "
                   "username if you want to receive Roles on Discord."),
        required=False,
    )
    
    
class DonationPriceForm(forms.Form):
    chosen_price = forms.IntegerField(
        label='Donation Amount',
        help_text=("Enter any whole amount you would like to donate "
                   "above the package's price."),
        required=False
    )


class DonationGatewayForm(forms.Form):
    payment_gateway = forms.ChoiceField(
        label='Payment Gateway',
        help_text='Choose your preferred way to pay.',
        widget=forms.RadioSelect,
        required=True,
        choices=[
            ('stripe', 'Stripe'),
            ('paypal', 'Paypal'),
        ], 
    )
