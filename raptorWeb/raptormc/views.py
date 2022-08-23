from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from os.path import join
from logging import getLogger

from raptorWeb import settings
from raptormc.util.playerCounts import PlayerCounts
from raptormc.forms import AdminApp, ModApp, UserForm, UserProfileInfoForm, UserLoginForm

TEMPLATE_DIR_RAPTORMC = join(settings.TEMPLATE_DIR, "raptormc")

player_poller = PlayerCounts()

LOGGER = getLogger(__name__)

class ShadowRaptor():
    """
    Object containing different categories of views that are used
    across the website/application.
    """
    class Info():
        """
        Views that act as static pages of information
        """
        def home_servers(request):
            """
            Homepage with general information
            """
            return render(request, join(TEMPLATE_DIR_RAPTORMC, "home.html"), context = player_poller.currentPlayers_DB)
        
        def rules(request):
            """
            Rules page containing general and server-specific rules
            """
            return render(request, join(TEMPLATE_DIR_RAPTORMC, 'rules.html'), context = player_poller.currentPlayers_DB)
            
        def banned_items(request):
            """
            Contains lists of items that are banned on each server
            """
            return render(request, join(TEMPLATE_DIR_RAPTORMC, 'banneditems.html'), context = player_poller.currentPlayers_DB)

        def apps(request):
            """
            Provide links to each staff application
            """
            return render(request, join(settings.APPLICATIONS_DIR, 'staffapps.html'), context=player_poller.currentPlayers_DB)
        
    class Application():
        """
        Views that contain forms and applications
        """
        def register(request):
            """
            User Registration form
            """
            registered = False

            register_form = UserForm()
            extra_form = UserProfileInfoForm()

            dictionary = player_poller.currentPlayers_DB
            dictionary["registered"] = registered
            dictionary["register_form"] = register_form
            dictionary["extra_form"] = extra_form

            if request.method == "POST":

                register_form = UserForm(request.POST)

                extra_form = UserProfileInfoForm(request.POST)

                dictionary["register_form"] = register_form
                dictionary["extra_form"] = extra_form

                if register_form.is_valid() and extra_form.is_valid():

                    LOGGER.error("[INFO] A new User has been registered!")
                    new_user = register_form.save()
                    new_user.set_password(new_user.password)
                    new_user.save()

                    new_user_extra = extra_form.save(commit=False)
                    new_user_extra.user = new_user

                    if "profile_picture" in request.FILES:

                        new_user_extra.profile_picture = request.FILES["profile_picture"]

                    new_user_extra.save()

                    registered = True
                    dictionary["registered"] = registered

                    return render(request, join(settings.APPLICATIONS_DIR, 'registration.html'), context=dictionary)

                else:

                    dictionary["register_form"] = register_form
                    dictionary["extra_form"] = extra_form

            return render(request, join(settings.APPLICATIONS_DIR, 'registration.html'), context=dictionary)
        
        def user_login(request):
            """
            User Login form
            """
            login_form = UserLoginForm()

            dictionary = player_poller.currentPlayers_DB

            dictionary["login_form"] = login_form

            if request.method == "POST":

                login_form = UserLoginForm(request.POST)

                if login_form.is_valid():

                    username = login_form.cleaned_data["username"]
                    password = login_form.cleaned_data["password"]

                    user = authenticate(username=username, password=password)

                    if user:

                        if user.is_active:

                            LOGGER.error("[INFO] User logged in!")
                            login(request, user)
                            return HttpResponseRedirect('..')

                        else:

                            return HttpResponse("Account not active")

                    else:

                        LOGGER.error("[INFO] User login attempt failed")
                        LOGGER.error("[INFO] Attempted User: {}".format(username))
                        dictionary["login_form"] = login_form

            return render(request, join(settings.APPLICATIONS_DIR, 'login.html'), context=dictionary)

        @login_required
        def user_logout(request):
            """
            Log out the signed in user
            """
            logout(request)
            LOGGER.error("[INFO] User logged out!")
            return HttpResponseRedirect('..')
        
        def mod_app(request):
            """
            Moderator Application
            """
            mod_app = ModApp()

            dictionary = player_poller.currentPlayers_DB

            dictionary["modform"] = mod_app

            if request.method == "POST":

                mod_app = ModApp(request.POST)

                if mod_app.is_valid():

                    LOGGER.error("[INFO] Mod Application submitted!")
                    LOGGER.error("[INFO] Discord ID of applicant: {}".format(mod_app.cleaned_data["discord_name"]))
                    new_app = mod_app.save()
                    return render(request, join(settings.APPLICATIONS_DIR, 'appsuccess.html'), context=dictionary)

                else:

                    dictionary["modform"] = mod_app

            return render(request, join(settings.APPLICATIONS_DIR, 'modapp.html'), context=dictionary)
            
        def admin_app(request):
            """
            Admin Application
            """         
            admin_app = AdminApp()

            dictionary = player_poller.currentPlayers_DB

            dictionary["admin_form"] = admin_app

            if request.method == "POST":

                admin_app = AdminApp(request.POST)

                if admin_app.is_valid():

                    LOGGER.error("[INFO] Admin Application submitted.!")
                    LOGGER.error("[INFO] Discord ID of applicant: {}".format(admin_app.cleaned_data["discord_name"]))
                    new_app = admin_app.save()
                    return render(request, join(settings.APPLICATIONS_DIR, 'appsuccess.html'), context=dictionary)

                else:

                    dictionary["admin_form"] = admin_app

            return render(request, join(settings.APPLICATIONS_DIR, 'adminapp.html'), context=dictionary)
