from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from os.path import join
from logging import getLogger

from raptorWeb import settings
from raptormc.util.playerCounts import PlayerCounts
from raptormc.forms import AdminApp, ModApp, UserForm, UserProfileInfoForm, UserLoginForm
from raptormc.models import InformativeText

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
        class HomeServers(TemplateView):
            """
            Homepage with general information
            """
            template_name = join(TEMPLATE_DIR_RAPTORMC, 'home.html')

            def get_context_data(self, **kwargs):
                context = super().get_context_data(**kwargs)
                context.update(player_poller.currentPlayers_DB)
                try:
                    context.update({
                        "home_info": InformativeText.objects.get(name="Homepage Information")
                    })
                except:
                    context.update({
                        "home_info": InformativeText.objects.create(name="Homepage Information", content="Update 'Homepage Information' Model to change this text")
                    })
                return context

        class Rules(TemplateView):
            """
            Rules page containing general and server-specific rules
            """
            template_name = join(TEMPLATE_DIR_RAPTORMC, 'rules.html')

            def get_context_data(self, **kwargs):
                context = super().get_context_data(**kwargs)
                context.update(player_poller.currentPlayers_DB)
                try:
                    context.update({
                        "rules_info": InformativeText.objects.get(name="Rules Information"),
                        "network_rules": InformativeText.objects.get(name="Network Rules")
                    })
                except:
                    context.update({
                        "rules_info": InformativeText.objects.create(name="Rules Information", content="Update 'Rules Information' Model to change this text"),
                        "network_rules": InformativeText.objects.create(name="Network Rules", content="Update 'Network Rules' Model to change this text")
                    })
                return context

        class BannedItems(TemplateView):
            """
            Contains lists of items that are banned on each server
            """
            template_name = join(TEMPLATE_DIR_RAPTORMC, 'banneditems.html')

            def get_context_data(self, **kwargs):
                context = super().get_context_data(**kwargs)
                context.update(player_poller.currentPlayers_DB)
                return context

        class StaffApps(TemplateView):
            """
            Provide links to each staff application
            """
            template_name = join(settings.APPLICATIONS_DIR, 'staffapps.html')

            def get_context_data(self, **kwargs):
                context = super().get_context_data(**kwargs)
                context.update(player_poller.currentPlayers_DB)
                return context
        
    class Application():
        """
        Views that contain forms and applications
        """
        class RegisterUser(TemplateView):

            template_name = join(settings.APPLICATIONS_DIR, 'registration.html')
            registered = False
            register_form = UserForm()
            extra_form = UserProfileInfoForm()

            def get(self, request):

                dictionary = player_poller.currentPlayers_DB
                dictionary["registered"] = self.registered
                dictionary["register_form"] = self.register_form
                dictionary["extra_form"] = self.extra_form
                
                return render(request, self.template_name, context=dictionary)

            def post(self,request):

                register_form = UserForm(request.POST)
                extra_form = UserProfileInfoForm(request.POST)

                dictionary = player_poller.currentPlayers_DB
                dictionary["registered"] = self.registered
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

                    return render(request, self.template_name, context=dictionary)

                else:

                    dictionary["register_form"] = register_form
                    dictionary["extra_form"] = extra_form

                    return render(request, self.template_name, context=dictionary)

        class UserLogin(TemplateView):
            """
            User Login form
            """
            template_name = join(settings.APPLICATIONS_DIR, 'login.html')
            login_form = UserLoginForm()

            def get(self, request):

                dictionary = player_poller.currentPlayers_DB
                dictionary["login_form"] = self.login_form
                
                return render(request, self.template_name, context=dictionary)      

            def post(self, request):

                login_form = UserLoginForm(request.POST)

                dictionary = player_poller.currentPlayers_DB
                dictionary["login_form"] = self.login_form

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

                        return render(request, self.template_name, context=dictionary)

        class ModApp(TemplateView):
            """
            Moderator Application
            """
            template_name = join(settings.APPLICATIONS_DIR, 'modapp.html')
            mod_app = ModApp()

            def get(self, request):

                dictionary = player_poller.currentPlayers_DB
                dictionary["modform"] = self.mod_app

                return render(request, self.template_name, context=dictionary)

            def post(self, request):

                mod_app = ModApp(request.POST)
                dictionary = player_poller.currentPlayers_DB
                dictionary["modform"] = mod_app

                if mod_app.is_valid():

                    LOGGER.error("[INFO] Mod Application submitted!")
                    LOGGER.error("[INFO] Discord ID of applicant: {}".format(mod_app.cleaned_data["discord_name"]))
                    new_app = mod_app.save()
                    return render(request, join(settings.APPLICATIONS_DIR, 'appsuccess.html'), context=dictionary)

                else:

                    dictionary["modform"] = mod_app

                    return render(request, self.template_name, context=dictionary)

        class AdminApp(TemplateView):
            """
            Admin Application
            """
            template_name = join(settings.APPLICATIONS_DIR, 'adminapp.html')
            admin_app = AdminApp()

            def get(self, request):

                dictionary = player_poller.currentPlayers_DB
                dictionary["admin_form"] = self.admin_app

                return render(request, self.template_name, context=dictionary)

            def post(self, request):

                admin_app = AdminApp(request.POST)
                dictionary = player_poller.currentPlayers_DB
                dictionary["admin_form"] = admin_app

                if admin_app.is_valid():

                    LOGGER.error("[INFO] Admin Application submitted.!")
                    LOGGER.error("[INFO] Discord ID of applicant: {}".format(admin_app.cleaned_data["discord_name"]))
                    new_app = admin_app.save()
                    return render(request, join(settings.APPLICATIONS_DIR, 'appsuccess.html'), context=dictionary)

                else:

                    dictionary["admin_form"] = admin_app

                    return render(request, self.template_name, context=dictionary)

        @login_required
        def user_logout(request):
            """
            Log out the signed in user
            """
            logout(request)
            LOGGER.error("[INFO] User logged out!")
            return HttpResponseRedirect('..')
            