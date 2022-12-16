from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from raptormc.models import User, UserProfileInfo, DiscordUserInfo

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