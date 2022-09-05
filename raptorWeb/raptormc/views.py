from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone
from os.path import join
from logging import getLogger
from json import load

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
                try:
                    announcementsJSON = open(join(settings.BASE_DIR, 'announcements.json'), "r")
                    context.update(load(announcementsJSON))
                except:
                    LOGGER.error("[ERROR][{}] announcements.json missing. Ensure Discord Bot is running and that your directories are structured correctly.".format(timezone.now().isoformat()))
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
                try:
                    context.update({
                        "banneditems_info": InformativeText.objects.get(name="Banned Items Information"),
                    })
                except:
                    context.update({
                        "banneditems_info": InformativeText.objects.create(name="Banned Items Information", content="Update 'Banned Items Information' Model to change this text"),
                    })
                return context

        class Voting(TemplateView):
            """
            Contains lists links for each server's voting sites
            """
            template_name = join(TEMPLATE_DIR_RAPTORMC, 'voting.html')

            def get_context_data(self, **kwargs):
                context = super().get_context_data(**kwargs)
                context.update(player_poller.currentPlayers_DB)
                try:
                    context.update({
                        "voting_info": InformativeText.objects.get(name="Voting Information"),
                    })
                except:
                    context.update({
                        "voting_info": InformativeText.objects.create(name="Voting Information", content="Update 'Voting Information' Model to change this text"),
                    })
                return context

        class HowToJoin(TemplateView):
            """
            Contains guides for downloading modpacks and joining servers.
            """
            template_name = join(TEMPLATE_DIR_RAPTORMC, 'joining.html')

            def get_context_data(self, **kwargs):
                context = super().get_context_data(**kwargs)
                context.update(player_poller.currentPlayers_DB)
                try:
                    context.update({
                        "joining_info": InformativeText.objects.get(name="Joining Information"),
                        "joining_curse_info": InformativeText.objects.get(name="Using the CurseForge Launcher"),
                        "joining_ftb_info": InformativeText.objects.get(name="Using the FTB Launcher"),
                        "joining_technic_info": InformativeText.objects.get(name="Using the Technic Launcher")
                    })
                except:
                    context.update({
                        "joining_info": InformativeText.objects.create(name="Joining Information", content="Update 'Joining Information' Model to change this text"),
                        "joining_curse_info": InformativeText.objects.create(name="Using the CurseForge Launcher", content="Update 'Using the CurseForge Launcher' Model to change this text"),
                        "joining_ftb_info": InformativeText.objects.create(name="Using the FTB Launcher", content="Update 'Using the FTB Launcher' Model to change this text"),
                        "joining_technic_info": InformativeText.objects.create(name="Using the Technic Launcher", content="Update 'Using the Technic Launcher' Model to change this text")
                    })
                return context

        class StaffApps(TemplateView):
            """
            Provide links to each staff application
            """
            template_name = join(settings.APPLICATIONS_DIR, 'staffapps.html')

            def get_context_data(self, **kwargs):
                context = super().get_context_data(**kwargs)
                context.update(player_poller.currentPlayers_DB)
                try:
                    context.update({
                        "staffapp_info": InformativeText.objects.get(name="Staff App Information"),
                    })
                except:
                    context.update({
                        "staffapp_info": InformativeText.objects.create(name="Staff App Information", content="Update 'Staff App Information' Model to change this text"),
                    })
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

                    LOGGER.error("[INFO][{}] A new User has been registered!".format(timezone.now().isoformat()))
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

                            LOGGER.error("[INFO][{}] User logged in!".format(timezone.now().isoformat()))
                            login(request, user)
                            return HttpResponseRedirect('..')

                        else:

                            return HttpResponse("Account not active")

                    else:

                        LOGGER.error("[INFO][{}] User login attempt failed".format(timezone.now().isoformat()))
                        LOGGER.error("[INFO][{}] Attempted User: {}".format(timezone.now().isoformat(), username))
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

                    LOGGER.error("[INFO][{}] Mod Application submitted!".format(timezone.now().isoformat()))
                    LOGGER.error("[INFO][{}] Discord ID of applicant: {}".format(timezone.now().isoformat(), mod_app.cleaned_data["discord_name"]))
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

                    LOGGER.error("[INFO][{}] Admin Application submitted.!".format(timezone.now().isoformat()))
                    LOGGER.error("[INFO][{}] Discord ID of applicant: {}".format(timezone.now().isoformat(), admin_app.cleaned_data["discord_name"]))
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
            LOGGER.error("[INFO][{}] User logged out!".format(timezone.now().isoformat()))
            return HttpResponseRedirect('..')
            