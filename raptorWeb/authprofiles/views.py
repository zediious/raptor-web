from os.path import join
from logging import Logger, getLogger

from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.core.mail import send_mail
from django.utils.text import slugify
from django.conf import settings

from raptorWeb.authprofiles.forms import UserRegisterForm, UserPasswordResetEmailForm, UserPasswordResetForm, UserProfileEditForm, UserLoginForm
from raptorWeb.authprofiles.models import RaptorUserManager, RaptorUser, DiscordUserInfo
from raptorWeb.authprofiles.tokens import RaptorUserTokenGenerator

LOGGER: Logger = getLogger('authprofiles.views')
AUTH_TEMPLATE_DIR: str = getattr(settings, 'AUTH_TEMPLATE_DIR')
DISCORD_AUTH_URL: str = getattr(settings, 'DISCORD_AUTH_URL')
LOGIN_URL: str = getattr(settings, 'LOGIN_URL')
BASE_USER_URL: str = getattr(settings, 'BASE_USER_URL')
USER_RESET_URL: str = getattr(settings, 'USER_RESET_URL')
DOMAIN_NAME: str = getattr(settings, 'DOMAIN_NAME')
WEB_PROTO: str = getattr(settings, 'WEB_PROTO')
EMAIL_HOST_USER: str = getattr(settings, 'EMAIL_HOST_USER')

token_generator: RaptorUserTokenGenerator = RaptorUserTokenGenerator()


class RegisterUser(TemplateView):
    """
    Returns a form for a user to register for the website with a username and
    password, creating a new RaptorUser.
    """
    template_name: str = join(AUTH_TEMPLATE_DIR, 'registration.html')
    registered: bool = False
    register_form: UserRegisterForm = UserRegisterForm

    def get(self, request: HttpRequest) -> HttpResponse:
        if request.headers.get('HX-Request') != "true":
            return HttpResponseRedirect('../')

        else:
            return render(request, self.template_name, context={
                "register_form": self.register_form,
                "registered": self.registered})

    def post(self, request: HttpRequest) -> HttpResponse:
        register_form: UserRegisterForm = self.register_form(request.POST)
        dictionary: dict = {"register_form": register_form}

        if register_form.is_valid():
            LOGGER.info("A new User has been registered!")
            RaptorUser.objects.create_user(register_form)
            self.registered = True
            dictionary["registered"] = self.registered
            return render(request, self.template_name, context=dictionary)

        else:
            return render(request, self.template_name, context=dictionary)


class UserResetPasswordForm(TemplateView):
    """
    Returns a form for a non-discord user to enter an email, which will
    send an email to submitted user's email detailing a password reset, if the
    submitted email and username matches a non-discord user's attributes.
    """
    password_reset_form: UserPasswordResetEmailForm = UserPasswordResetEmailForm
    template_name: str = join(AUTH_TEMPLATE_DIR, 'password_reset_email_form.html')

    def get(self, request: HttpRequest) -> HttpResponse:
        if request.headers.get('HX-Request') != "true":
            return HttpResponseRedirect('../')

        else:
            return render(request, self.template_name, context={
                "password_reset_form": self.password_reset_form})

    def post(self, request: HttpRequest) -> HttpResponse:
        password_reset_form: UserPasswordResetEmailForm = self.password_reset_form(request.POST)
        dictionary: dict = {"password_reset_form": password_reset_form}

        if password_reset_form.is_valid():
            resetting_user: RaptorUser = RaptorUser.objects.get(
                username = password_reset_form.cleaned_data["username"],
                email = password_reset_form.cleaned_data["email"])
            if resetting_user.is_discord_user == True:
                messages.error(request, "Discord users cannot reset their password")
                return render(request, self.template_name, context=dictionary)

            resetting_user.password_reset_token = token_generator.make_token(resetting_user)
            resetting_user.save()
            send_mail(subject=f"User password reset for: {resetting_user.username}",
                message=("Click the following link to enter a password reset form for your account: "
                        f"{WEB_PROTO}://{DOMAIN_NAME}/"
                        f"{BASE_USER_URL}/{USER_RESET_URL}/"
                        f"{resetting_user.user_slug}/{resetting_user.password_reset_token}"),
                from_email=EMAIL_HOST_USER,
                recipient_list=[resetting_user.email]
            )
            LOGGER.info(f"Password reset submitted for {resetting_user.username}. Email has been sent.")
            messages.error(request, "Await reset link at user email")
            return render(request, self.template_name, context=dictionary)

        else:
            return render(request, self.template_name, context=dictionary)


class UserResetPasswordConfirm(TemplateView):
    """
    View returned from password reset links emailed to users. Will confirm that
    token in PATH matches user's reset token, then return form to reset password.
    """
    final_password_reset_form: UserPasswordResetForm = UserPasswordResetForm
    template_name: str = join(AUTH_TEMPLATE_DIR, 'password_reset_form.html')

    def get(self, request: HttpRequest, user_reset_token: str) -> HttpResponse:
        if request.headers.get('HX-Request') != "true":
            return HttpResponseRedirect('../')

        else:
            try:
                resetting_user: RaptorUser = RaptorUser.objects.get(
                                        password_reset_token=user_reset_token)
                if resetting_user.password_reset_token == "":
                    return redirect('/accessdenied')

                return render(request, self.template_name, context={
                    "final_password_reset_form": self.final_password_reset_form,
                    "resetting_user_token": resetting_user.password_reset_token})

            except RaptorUser.DoesNotExist:
                return redirect('/accessdenied')

    def post(self, request: HttpRequest, user_reset_token: str) -> HttpResponse:
        final_password_reset_form: UserPasswordResetForm = self.final_password_reset_form(request.POST)
        resetting_user = RaptorUser.objects.get(password_reset_token=str(user_reset_token))
        dictionary: dict = {"final_password_reset_form": final_password_reset_form}
        dictionary["resetting_user_token"]: str = resetting_user.password_reset_token

        if final_password_reset_form.is_valid():
            resetting_user.set_password(final_password_reset_form.cleaned_data["password"])
            resetting_user.password_reset_token = ""
            resetting_user.save()
            LOGGER.info(f"User: {resetting_user.username} has reset their password")
            return render(request, join(AUTH_TEMPLATE_DIR, 'reset_successful.html'), context=dictionary)

        else:
            return render(request, self.template_name, context=dictionary)


class User_Login_Form(TemplateView):
    """
    Returns a form for a user to login with Username and Password
    """
    login_form: UserLoginForm = UserLoginForm()
    template_name: str = join(AUTH_TEMPLATE_DIR, 'login.html')

    def get(self, request: HttpRequest) -> HttpResponse:
        if request.headers.get('HX-Request') == "true":
            return render(request, self.template_name, context={"login_form": self.login_form})

        else:
            return HttpResponseRedirect('../')

    def post(self, request: HttpRequest) -> HttpResponse:
        login_form: UserLoginForm = UserLoginForm(request.POST)

        if login_form.is_valid():
            username: str = login_form.cleaned_data["username"]
            password: str = login_form.cleaned_data["password"]
            user: RaptorUser = authenticate(username=username, password=password)
            if user:
                LOGGER.info(f"{username} logged in!")
                login(request, user)
                return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))

            else:
                return HttpResponse("Account does not exist")

        else:
            messages.error(request, login_form.errors.as_text().replace('* __all__', ''))
            return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))


class UserLogin_OAuth(TemplateView):
    """
    View to redirect users to Discord OAuth2 endpoint.
    """
    def get(self, request: HttpRequest) -> HttpResponse:
        return redirect(DISCORD_AUTH_URL)


class UserLogin_OAuth_Success(TemplateView):
    """
    View returned when a User authenticates with Discord OAuth2 successfully.
    Will log in an existing user, or create an account if they do not have one.
    """
    def get(self, request: HttpRequest) -> HttpResponse:
        try:
            discord_code = request.GET.get('code')
            user_info = RaptorUser.objects.exchange_discord_code(discord_code)
            discord_user = authenticate(request,user=user_info)
            RaptorUser.objects.update_discord_user_details(
                DiscordUserInfo.objects.get(id=user_info["id"]),
                user_info)
            LOGGER.info(f'{user_info["username"]} logged in')
            login(request, 
                discord_user,
                backend='raptorWeb.authprofiles.auth.DiscordAuthBackend')
            return redirect('/')
            
        except KeyError:
            return HttpResponseRedirect("/")


@login_required
def user_logout(request: HttpRequest) -> HttpResponse:
    """
    Log out the signed in user
    """
    logout(request)
    LOGGER.info(f"{request.user} logged out!")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class User_Dropdown(TemplateView):
    """
    Dropdown Button with User Picture and Links
    """
    template_name: str = join(AUTH_TEMPLATE_DIR, 'profile_dropdown.html')

    def get(self, request: HttpRequest) -> HttpResponse:
        if request.headers.get('HX-Request') == "true":
            instance_dict: dict = {}
            if request.user.is_authenticated:
                instance_dict['loaded_user']: RaptorUser = RaptorUser.objects.get(
                    user_slug = RaptorUser.objects.find_slugged_user(str(request.user)).user_slug)

            return render(request, self.template_name, context=instance_dict)

        else:
            return HttpResponseRedirect('/')


class All_User_Profile(ListView):
    """
    ListView for all Users
    """
    paginate_by: int = 9
    model: RaptorUser = RaptorUser
    queryset: RaptorUserManager = RaptorUser.objects.order_by('-date_joined')

    def get(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        if request.headers.get('HX-Request') == "true":
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/')


class User_Profile(DetailView):
    """
    DetailView for a User's profile
    """
    model: RaptorUser = RaptorUser

    def get(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        if request.headers.get('HX-Request') == "true":
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/')

    def get_object(self):
        return RaptorUser.objects.get(user_slug = self.kwargs['user_slug'])


class User_Profile_Edit(LoginRequiredMixin, TemplateView):
    """
    Return a form displaying a User's profile details that can be edited
    and allow changing of said details.
    """
    template_name: str = join(AUTH_TEMPLATE_DIR, 'profile_edit.html')
    login_url: str = LOGIN_URL
    extra_edit_form: UserProfileEditForm = UserProfileEditForm()

    def get(self, request: HttpRequest, profile_name: str) -> HttpResponse:
        if request.headers.get('HX-Request') == "true":
            if slugify(str(request.user)) == slugify(profile_name):
                instance_dict: dict = {"extra_edit_form": self.extra_edit_form}
                displayed_user: RaptorUser = RaptorUser.objects.find_slugged_user(profile_name)
                if displayed_user != None:
                    instance_dict["displayed_profile"] = displayed_user
                    return render(request, self.template_name, context=instance_dict)

                else:
                    return redirect('/nouserfound')

            else: 
                return redirect('/accessdenied')

        else:
            return HttpResponseRedirect('/')

    def post(self, request: HttpRequest, profile_name: str) -> HttpResponse:
        extra_edit_form: UserProfileEditForm = UserProfileEditForm(request.POST, request.FILES)
        instance_dict: dict = {"extra_edit_form": extra_edit_form}
        instance_dict["displayed_profile"] = RaptorUser.objects.find_slugged_user(profile_name)

        if extra_edit_form.is_valid():
            changed_user: RaptorUser = RaptorUser.objects.update_user_profile_details(
                extra_edit_form, 
                request)
            LOGGER.info(f"{changed_user.username} modified their profile details")
            messages.error(request, "Profile details successfully changed!")
            return render(request, self.template_name, context=instance_dict)

        else:
            return render(request, self.template_name, context=instance_dict)


class Access_Denied(TemplateView):
    """
    Page displayed when a resource cannot be accessed by a user
    """
    template_name: str = join(AUTH_TEMPLATE_DIR, 'no_access.html')

    def get(self, request):
        if request.headers.get('HX-Request') == "true":
            return render(request, self.template_name, context={})

        else:
            return HttpResponseRedirect('/')

class No_User_Found(TemplateView):
    """
    Page displayed when a requested user is not found
    """
    template_name: str = join(AUTH_TEMPLATE_DIR, 'no_user.html')

    def get(self, request):
        if request.headers.get('HX-Request') == "true":
            return render(request, self.template_name, context={})

        else:
            return HttpResponseRedirect('../')
