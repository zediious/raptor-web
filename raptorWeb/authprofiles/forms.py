from django import forms
from django.contrib.auth import authenticate
from django.core.files.uploadedfile import InMemoryUploadedFile

from captcha.fields import CaptchaField

from raptorWeb.authprofiles.models import RaptorUserManager, RaptorUser, UserProfileInfo


def check_profile_picture_dimensions(image: InMemoryUploadedFile) -> bool:
    """
    Check if an image's aspect ratio is 1x1 or very close to.
    Will return True if so. Return False if not.
    """
    if image.image.width > image.image.height:
        if (abs(image.image.width-image.image.height) / image.image.height) * 100 <= 30:
            return True

        return False

    elif image.image.height > image.image.width:
        if (abs(image.image.height-image.image.width) / image.image.width) * 100 <= 30:
            return True

        return False

    return True


class UserRegisterForm(forms.ModelForm):
    """
    Form returned for registering a user with a password
    """
    password: forms.CharField = forms.CharField(widget=forms.PasswordInput())
    password_v: forms.CharField = forms.CharField(label="Verify Password", widget=forms.PasswordInput())
    captcha: CaptchaField = CaptchaField()

    class Meta():
        model: RaptorUser = RaptorUser
        fields: tuple[str] = ('username', 'email', 'password')

    def clean(self):
        """
        Overrides default clean, while calling the superclass clean()
        Ensures password fields are the same.
        """
        clean_data: dict = super().clean()

        if not(clean_data.get("password") == clean_data.get("password_v")):
            raise forms.ValidationError("Password fields must match")

class UserProfileEditForm(forms.ModelForm):
    """
    Form returned for editing profile information
    """  
    captcha: CaptchaField = CaptchaField()
    picture_changed_manually: forms.BooleanField = forms.BooleanField(
        label = "Reset Profile Picture",
        help_text = "If this is checked, your Profile Picture will be reset to your current Discord Avatar. This setting has no effect for Users that did not sign up with Discord.",
        required = False
    )
    reset_toasts: forms.BooleanField = forms.BooleanField(
        label = "Reset Seen Notification Toasts",
        help_text = "If this is checked, your user data about what notification toasts you have seen will be erased, and you will see all of them again.",
        required = False
    )
    hidden_from_public: forms.BooleanField = forms.BooleanField(
        label = "Hidden from Public",
        help_text="Indicates whether your profile appears on the user list, and whether it is publicly accessible.",
        required = False
    )

    class Meta():
        model: UserProfileInfo = UserProfileInfo
        fields: tuple[str] = ('hidden_from_public', 'reset_toasts', 'picture_changed_manually', 'profile_picture', 'minecraft_username', 'favorite_modpack')

    def clean(self):
        """
        Overrides default clean, while calling the superclass clean()
        Check image dimensions of profile picture
        """
        clean_data: dict = super().clean()
        image: InMemoryUploadedFile = clean_data.get('profile_picture')
        if image != None:
            if check_profile_picture_dimensions(image) == False:
                raise forms.ValidationError("Aspect ratio of profile picture must be relatively close to 1x1.")

class UserLoginForm(forms.Form):
    """
    Form returned for logging into a user with a password
    """
    username: forms.CharField = forms.CharField(max_length=100)
    password: forms.CharField = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        """
        Overrides default clean, while calling the superclass clean()
        Ensures a User exists and that password is correct before 
        returning clean data to view
        """
        clean_data: dict = super().clean()
        username: str = clean_data.get("username")
        password: str = clean_data.get("password")

        try:
            queried_user: RaptorUser = RaptorUser.objects.get(username=username)
            
            if queried_user.is_discord_user == True:
                raise forms.ValidationError("The entered Password was incorrect")

            if authenticate(username=username, password=password) == None:
                raise forms.ValidationError("The entered Password was incorrect")

        except RaptorUser.DoesNotExist:
            raise forms.ValidationError("The entered Password was incorrect")

class UserPasswordResetEmailForm(forms.Form):
    """
    Form returned for sending a password reset email
    """
    username: forms.CharField = forms.CharField()
    email: forms.CharField = forms.EmailField(widget=forms.EmailInput())
    captcha: CaptchaField = CaptchaField()

    def clean(self):
        """
        Ensure a user with supplied username and email exists
        """
        clean_data: dict = super().clean()
        username: str = clean_data.get("username")
        email: str = clean_data.get("email")
        found_user: RaptorUserManager = RaptorUser.objects.filter(username = username, email = email)

        if found_user.count() == 0:
            raise forms.ValidationError("No user with submitted username and email exists")

        elif found_user.count() > 1:
            raise forms.ValidationError("There was an error processing this request, please contact a site admin.")

class UserPasswordResetForm(forms.Form):
    """
    Form returned for resetting a non-discord user's password
    """
    password: forms.CharField = forms.CharField(label="Enter your new password", widget=forms.PasswordInput())
    password_v: forms.CharField = forms.CharField(label="Verify Password", widget=forms.PasswordInput())
    captcha: CaptchaField = CaptchaField()

    def clean(self):
        """
        Ensure new password fields match
        """
        clean_data: dict = super().clean()

        if not(clean_data.get("password") == clean_data.get("password_v")):
            raise forms.ValidationError("Password fields must match")
        
        
class UserListFilter(forms.Form):
    """
    Form returned to filter the user list
    """
    is_staff: forms.BooleanField = forms.BooleanField(
        label="Is Staff",
        required=False)
    
    username: forms.CharField = forms.CharField(
        label="Username",
        required=False
    )

         