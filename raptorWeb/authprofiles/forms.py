from django import forms
from django.contrib.auth import authenticate

from captcha.fields import CaptchaField

from raptorWeb.authprofiles.models import RaptorUser, UserProfileInfo
from raptorWeb.authprofiles.util.usergather import find_slugged_user, check_profile_picture_dimensions

class UserRegisterForm(forms.ModelForm):
    """
    Form returned for registering a user with a password
    """
    password = forms.CharField(widget=forms.PasswordInput())
    password_v = forms.CharField(label="Verify Password", widget=forms.PasswordInput())
    captcha = CaptchaField()

    class Meta():
        model = RaptorUser
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

class UserLoginForm(forms.Form):
    """
    Form returned for logging into a user with a password
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

        if find_slugged_user(username).is_discord_user:
            raise forms.ValidationError("The entered Username does not exist")

        for user in RaptorUser.objects.all():
            if user.username == username:
                user_exists = True
                break

        if user_exists == False:
            raise forms.ValidationError("The entered Username does not exist")

        if authenticate(username=username, password=password) == None:
            raise forms.ValidationError("The entered Password was incorrect")

class UserProfileEditForm(forms.ModelForm):
    """
    Form returned for editing profile information
    """  
    captcha = CaptchaField()

    picture_changed_manually = forms.BooleanField(
        label = "Reset Profile Picture",
        help_text="If this is checked, your Profile Picture will be reset to your current Discord Avatar. This setting has no effect for Users that did not sign up with Discord.",
        required=False
    )

    class Meta():
        model = UserProfileInfo
        fields = ('picture_changed_manually', 'profile_picture', 'minecraft_username', 'favorite_modpack')

    def clean(self):
        """
        Overrides default clean, while calling the superclass clean()
        Check image dimensions of profile picture
        """
        clean_data = super().clean()
        image = clean_data.get('profile_picture')
        if image != None:
            if check_profile_picture_dimensions(image) == False:
                raise forms.ValidationError("Aspect ratio of profile picture must be relatively close to 1x1.")