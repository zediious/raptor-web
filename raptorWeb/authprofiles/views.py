from os.path import join
from logging import getLogger

from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.utils.text import slugify
from django.conf import settings

from raptorWeb.authprofiles.forms import UserRegisterForm, UserProfileEditForm, UserLoginForm
from raptorWeb.authprofiles.models import RaptorUser, UserProfileInfo, DiscordUserInfo
from raptorWeb.authprofiles.util import discordAuth
from raptorWeb.authprofiles.util.usergather import find_slugged_user

LOGGER = getLogger('authprofiles.views')
AUTH_TEMPLATE_DIR = getattr(settings, 'AUTH_TEMPLATE_DIR')
DISCORD_AUTH_URL = getattr(settings, 'DISCORD_AUTH_URL')
BASE_USER_URL = getattr(settings, 'BASE_USER_URL')

class RegisterUser(TemplateView):

    template_name = join(AUTH_TEMPLATE_DIR, 'registration.html')
    registered = False
    register_form = UserRegisterForm()
    extra_form = UserProfileEditForm()

    def get(self, request):

        if request.headers.get('HX-Request') == "true":
            dictionary = {}
            dictionary['user_path'] = BASE_USER_URL
            dictionary["registered"] = self.registered
            dictionary["register_form"] = self.register_form
            dictionary["extra_form"] = self.extra_form
            
            return render(request, self.template_name, context=dictionary)

        else:
            return HttpResponseRedirect('../')

    def post(self,request):

        register_form = UserRegisterForm(request.POST)
        extra_form = UserProfileEditForm(request.POST)

        dictionary = {}
        dictionary['user_path'] = BASE_USER_URL
        dictionary["registered"] = self.registered
        dictionary["register_form"] = register_form
        dictionary["extra_form"] = extra_form
        

        if register_form.is_valid() and extra_form.is_valid():

            LOGGER.info("A new User has been registered!")
            new_user = register_form.save()
            new_user.set_password(new_user.password)
            new_user_extra = extra_form.save(commit=False)
            new_user_extra.user = new_user
            if "profile_picture" in request.FILES:
                new_user_extra.profile_picture = request.FILES["profile_picture"]
            new_user.user_slug = slugify(new_user.username)
            new_user_extra.save()
            new_user.user_profile_info = new_user_extra
            new_user.save()
            registered = True
            dictionary["registered"] = registered
            login(request, new_user, backend='django.contrib.auth.backends.ModelBackend')
            return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))

        else:

            dictionary["register_form"] = register_form
            dictionary["extra_form"] = extra_form
            messages.error(request, register_form.errors.as_text().replace('* __all__', ''))
            return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))

class User_Login_Form(TemplateView):
    """
    Returns a form for a user to login with Username and Password
    """
    login_form = UserLoginForm()

    def get(self, request):

        if request.headers.get('HX-Request') == "true":
            dictionary = {}
            dictionary['user_path'] = BASE_USER_URL
            dictionary["login_form"] = self.login_form
            template_name = join(AUTH_TEMPLATE_DIR, 'login.html')
            return render(request, template_name, context=dictionary)
        else:
            return HttpResponseRedirect('../')

    def post(self, request):

        login_form = UserLoginForm(request.POST)
        dictionary = {}
        dictionary['user_path'] = BASE_USER_URL
        dictionary["login_form"] = self.login_form

        if login_form.is_valid():
            username = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
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

    def get(self, request):
        return redirect(DISCORD_AUTH_URL)

class UserLogin_OAuth_Success(TemplateView):

    def get(self, request):

        try:
            discord_code = request.GET.get('code')
            user_info = discordAuth.exchange_code(discord_code)
            discord_user = authenticate(request, user=user_info)
            discordAuth.update_user_details(DiscordUserInfo.objects.get(id=user_info["id"]), user_info)
            LOGGER.info(f'{user_info["username"]} logged in')
            try:
                login(request, discord_user, backend='raptorWeb.authprofiles.auth.DiscordAuthBackend')
            except AttributeError:
                login(request, list(discord_user).pop(), backend='raptorWeb.authprofiles.auth.DiscordAuthBackend')
            return redirect('../../')
        except KeyError:
            return HttpResponseRedirect("../login")

@login_required
def user_logout(request):
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
    template_name = join(AUTH_TEMPLATE_DIR, 'profile_dropdown.html')

    def get(self, request):
        if request.headers.get('HX-Request') == "true":
            instance_dict = {}
            instance_dict['user_path'] = BASE_USER_URL
            if request.user.is_authenticated:
                instance_dict['loaded_user'] = RaptorUser.objects.get(
                    user_slug = find_slugged_user(str(request.user)).user_slug)
            return render(request, self.template_name, context=instance_dict)
        else:
            return HttpResponseRedirect('../')

class All_User_Profile(ListView):
    """
    ListView for all Users
    """
    model = RaptorUser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        if request.headers.get('HX-Request') == "true":
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('../')

class User_Profile(DetailView):
    """
    DetailView for a User's profile
    """
    model = RaptorUser

    def get(self, request, *args, **kwargs):
        if request.headers.get('HX-Request') == "true":
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('../../')

    def get_object(self):
        return RaptorUser.objects.get(user_slug = slugify(self.request.GET.get('requested_user')))

class User_Profile_Edit(LoginRequiredMixin, TemplateView):
    """
    Displays a User's profile details that can be edited, and allows
    changing of said details
    """
    template_name = join(AUTH_TEMPLATE_DIR, 'profile_edit.html')
    login_url = '/login/'
    extra_edit_form = UserProfileEditForm()

    def get(self, request, profile_name):
        if request.headers.get('HX-Request') == "true":
            if slugify(str(request.user)) == slugify(profile_name):
                instance_dict = {}
                instance_dict['user_path'] = BASE_USER_URL
                instance_dict["extra_edit_form"] = self.extra_edit_form
                displayed_user = find_slugged_user(profile_name)

                if displayed_user == None:
                    return redirect('/nouserfound')
                else:
                    instance_dict.update({
                                "displayed_profile": displayed_user
                            })

                    return render(request, self.template_name, context=instance_dict)

            else: 
                return redirect('/accessdenied')

        else:
            return HttpResponseRedirect('../../../')

    def post(self, request, profile_name):

        extra_edit_form = UserProfileEditForm(request.POST)
        instance_dict = {}
        instance_dict['user_path'] = BASE_USER_URL
        instance_dict["extra_edit_form"] = self.extra_edit_form
        if extra_edit_form.is_valid():
            changed_user = RaptorUser.objects.get(username=request.user)
            if extra_edit_form.cleaned_data["minecraft_username"] != '':
                changed_user.user_profile_info.minecraft_username = extra_edit_form.cleaned_data["minecraft_username"]
            if extra_edit_form.cleaned_data["favorite_modpack"] != '':
                changed_user.user_profile_info.favorite_modpack = extra_edit_form.cleaned_data["favorite_modpack"]
            if "profile_picture" in request.FILES:
                changed_user.user_profile_info.profile_picture = request.FILES["profile_picture"]
                changed_user.user_profile_info.picture_changed_manually = True
            changed_user.user_profile_info.save()
            changed_user.save()
            LOGGER.info(f"{changed_user.username} modified their profile details")
            return redirect(f'../../../{BASE_USER_URL}/{slugify(changed_user.username)}')
        else:
            instance_dict["extra_edit_form"] = extra_edit_form
            return render(request, self.template_name, context=instance_dict)

class Access_Denied(TemplateView):
    """
    Page displayed when a resource cannot be accessed by a user
    """
    template_name = join(AUTH_TEMPLATE_DIR, 'no_access.html')

    def get(self, request):

        if request.headers.get('HX-Request') == "true":
            dictionary = {}
            dictionary['user_path'] = BASE_USER_URL
            return render(request, self.template_name, context=dictionary)
        else:
            return HttpResponseRedirect('../')

class No_User_Found(TemplateView):
    """
    Page displayed when a requested user is not found
    """
    template_name = join(AUTH_TEMPLATE_DIR, 'no_user.html')

    def get(self, request):

        if request.headers.get('HX-Request') == "true":
            dictionary = {}
            dictionary['user_path'] = BASE_USER_URL
            return render(request, self.template_name, context=dictionary)
        else:
            return HttpResponseRedirect('../')
