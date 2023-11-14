from os.path import join
from logging import Logger, getLogger
from typing import Any

from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.utils.text import slugify
from django.conf import settings

from raptorWeb.authprofiles.forms import UserRegisterForm, UserPasswordResetEmailForm, UserPasswordResetForm, UserProfileEditForm, UserLoginForm
from raptorWeb.authprofiles.models import RaptorUserManager, RaptorUser
from raptorWeb.authprofiles.tokens import RaptorUserTokenGenerator

try:
    from raptorWeb.raptormc.models import DefaultPages
except ModuleNotFoundError:
    pass

LOGGER: Logger = getLogger('authprofiles.views')
AUTH_TEMPLATE_DIR: str = getattr(settings, 'AUTH_TEMPLATE_DIR')
DISCORD_AUTH_URL: str = getattr(settings, 'DISCORD_AUTH_URL')
LOGIN_URL: str = getattr(settings, 'LOGIN_URL')
BASE_USER_URL: str = getattr(settings, 'BASE_USER_URL')

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
            email_sent = RaptorUser.objects.send_reset_email(password_reset_form)
            if email_sent == False:
                messages.error(request, "Discord users cannot reset their password")
                return render(request, self.template_name, context=dictionary)
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
                    return render(request, join(AUTH_TEMPLATE_DIR, 'no_access.html'), context={})

                return render(request, self.template_name, context={
                    "final_password_reset_form": self.final_password_reset_form,
                    "resetting_user_token": resetting_user.password_reset_token})

            except RaptorUser.DoesNotExist:
                return render(request, join(AUTH_TEMPLATE_DIR, 'no_access.html'), context={})

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
            discord_user.discord_user_info.update_discord_user_details(
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
    LOGGER.info(f"{request.user} logging out!")
    logout(request)
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
    queryset: RaptorUserManager = RaptorUser.objects.filter(is_superuser = False).order_by('-date_joined')

    def get(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        try:
            if not DefaultPages.objects.get_or_create(pk=1)[0].members:
                return HttpResponseRedirect('/404')
            
        except ModuleNotFoundError:
            pass
        
        if request.headers.get('HX-Request') != "true":
            return HttpResponseRedirect('/')
        
        else:
            if request.GET.get('is_staff') == 'on':
                self.queryset = self.queryset.filter(is_staff=True)
                
            if request.GET.get('username'):
                self.queryset = self.queryset.filter(username__contains=request.GET.get('username'))
                
            return super().get(request, *args, **kwargs)
        
    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context.update(
            {
                "base_user_url": BASE_USER_URL
            }
        )
        return context


class User_Profile(DetailView):
    """
    DetailView for a User's profile
    """
    model: RaptorUser = RaptorUser

    def get(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        try:
            if not DefaultPages.objects.get_or_create(pk=1)[0].members:
                if (request.headers.get('HX-Request') == "true"
                and request.user.user_slug == self.kwargs['user_slug']
                or request.user.is_staff):
                    return super().get(request, *args, **kwargs)
                
                else:
                    return render(request, join(AUTH_TEMPLATE_DIR, 'no_user.html'), context={})
                
        except AttributeError:
            return render(request, join(AUTH_TEMPLATE_DIR, 'no_user.html'), context={})
            
        except ModuleNotFoundError:
            pass
        
        if request.headers.get('HX-Request') == "true":
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/')

    def get_object(self):
        try:
            return RaptorUser.objects.get(user_slug = self.kwargs['user_slug'])
        
        except RaptorUser.DoesNotExist:
            return False


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
                    return render(request, join(AUTH_TEMPLATE_DIR, 'no_user.html'), context={})

            else: 
                return render(request, join(AUTH_TEMPLATE_DIR, 'no_access.html'), context={})

        else:
            return HttpResponseRedirect('/')

    def post(self, request: HttpRequest, profile_name: str) -> HttpResponse:
        extra_edit_form: UserProfileEditForm = UserProfileEditForm(request.POST, request.FILES)
        instance_dict: dict = {"extra_edit_form": extra_edit_form}
        instance_dict["displayed_profile"] = RaptorUser.objects.find_slugged_user(profile_name)

        if extra_edit_form.is_valid():
            self.request.user.user_profile_info.update_user_profile_details(
                extra_edit_form,
                request.FILES
            )
            LOGGER.info(f"{self.request.user.username} modified their profile details")
            messages.success(request, "Profile details successfully changed!")
            return render(request, self.template_name, context=instance_dict)

        else:
            return render(request, self.template_name, context=instance_dict)
