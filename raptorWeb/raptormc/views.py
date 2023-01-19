from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from os.path import join
from logging import getLogger
from json import load

from raptorWeb import settings
from raptormc.forms import AdminApp, ModApp, UserForm, UserProfileInfoForm, UserLoginForm, DiscordUserInfoForm
from raptormc.models import InformativeText, User, UserProfileInfo, DiscordUserInfo
from raptormc.jobs import player_poller, playerPoll, export_server_data_full
from raptormc.util import discordAuth, viewContext

TEMPLATE_DIR_RAPTORMC = join(settings.TEMPLATE_DIR, "raptormc")

LOGGER = getLogger('raptormc.views')

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
                return viewContext.update_context(context = context, informative_text_names = ["Homepage Information"], announcements=True)

        class Announcements(TemplateView):
            """
            Page containing the last 30 announcements from Discord
            """
            template_name = join(TEMPLATE_DIR_RAPTORMC, 'announcements.html')

            def get_context_data(self, **kwargs):
                context = super().get_context_data(**kwargs)
                context.update(player_poller.currentPlayers_DB)
                return viewContext.update_context(context = context, informative_text_names = ["Announcements Information"], announcements=True)

        class Rules(TemplateView):
            """
            Rules page containing general and server-specific rules
            """
            template_name = join(TEMPLATE_DIR_RAPTORMC, 'rules.html')

            def get_context_data(self, **kwargs):
                context = super().get_context_data(**kwargs)
                context.update(player_poller.currentPlayers_DB)
                return viewContext.update_context(context = context, informative_text_names = [
                    "Rules Information",
                    "Network Rules"])

        class BannedItems(TemplateView):
            """
            Contains lists of items that are banned on each server
            """
            template_name = join(TEMPLATE_DIR_RAPTORMC, 'banneditems.html')

            def get_context_data(self, **kwargs):
                context = super().get_context_data(**kwargs)
                context.update(player_poller.currentPlayers_DB)
                return viewContext.update_context(context = context, informative_text_names = ["Banned Items Information"])

        class Voting(TemplateView):
            """
            Contains lists links for each server's voting sites
            """
            template_name = join(TEMPLATE_DIR_RAPTORMC, 'voting.html')

            def get_context_data(self, **kwargs):
                context = super().get_context_data(**kwargs)
                context.update(player_poller.currentPlayers_DB)
                return viewContext.update_context(context = context, informative_text_names = ["Voting Information"])

        class HowToJoin(TemplateView):
            """
            Contains guides for downloading modpacks and joining servers.
            """
            template_name = join(TEMPLATE_DIR_RAPTORMC, 'joining.html')

            def get_context_data(self, **kwargs):
                context = super().get_context_data(**kwargs)
                context.update(player_poller.currentPlayers_DB)
                return viewContext.update_context(context = context, informative_text_names = [
                    "Joining Information",
                    "Using the CurseForge Launcher",
                    "Using the FTB Launcher",
                    "Using the Technic Launcher"])

        class StaffApps(TemplateView):
            """
            Provide links to each staff application
            """
            template_name = join(settings.APPLICATIONS_DIR, 'staffapps.html')

            def get_context_data(self, **kwargs):
                context = super().get_context_data(**kwargs)
                context.update(player_poller.currentPlayers_DB)
                return viewContext.update_context(context = context, informative_text_names = ["Staff App Information"])
        
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
                dictionary = viewContext.update_context(context = dictionary)
                
                return render(request, self.template_name, context=dictionary)

            def post(self,request):

                register_form = UserForm(request.POST)
                extra_form = UserProfileInfoForm(request.POST)

                dictionary = player_poller.currentPlayers_DB
                dictionary["registered"] = self.registered
                dictionary["register_form"] = register_form
                dictionary["extra_form"] = extra_form
                dictionary = viewContext.update_context(context = dictionary)

                if register_form.is_valid() and extra_form.is_valid():

                    LOGGER.info("A new User has been registered!")
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

        class User_Login_Form(TemplateView):
            """
            Returns a form for a user to login with Username and Password
            """
            login_form = UserLoginForm()

            def get(self, request):

                if request.headers.get('HX-Request') == "true":
                    dictionary = player_poller.currentPlayers_DB
                    dictionary["login_form"] = self.login_form
                    template_name = join(settings.APPLICATIONS_DIR, 'login.html')
                    return render(request, template_name, context=dictionary)
                else:
                    return HttpResponseRedirect('../')

            def post(self, request):

                login_form = UserLoginForm(request.POST)
                dictionary = player_poller.currentPlayers_DB
                dictionary["login_form"] = self.login_form

                if login_form.is_valid():
                    username = login_form.cleaned_data["username"]
                    password = login_form.cleaned_data["password"]
                    user = authenticate(username=username, password=password)
                    if user:
                        LOGGER.info("User logged in!")
                        login(request, user)
                        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))
                    else:
                        return HttpResponse("Account does not exist")
                else:
                    messages.error(request, login_form.errors.as_text().replace('* __all__', ''))
                    return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))

        class UserLogin_OAuth(TemplateView):

            def get(self, request):
                return redirect(settings.DISCORD_AUTH_URL)

        class UserLogin_OAuth_Success(TemplateView):

            def get(self, request):

                try:
                    discord_code = request.GET.get('code')
                    user_info = discordAuth.exchange_code(discord_code)
                    discord_user = authenticate(request, user=user_info)
                    try:
                        login(request, discord_user, backend='raptormc.auth.DiscordAuthBackend')
                    except AttributeError:
                        login(request, list(discord_user).pop(), backend='raptormc.auth.DiscordAuthBackend')
                    return redirect('../../')
                except KeyError:
                    return HttpResponseRedirect("../login")

        class ModApp(TemplateView):
            """
            Moderator Application
            """
            template_name = join(settings.APPLICATIONS_DIR, 'modapp.html')
            mod_app = ModApp()

            def get(self, request):
                dictionary = player_poller.currentPlayers_DB
                dictionary["modform"] = self.mod_app
                dictionary = viewContext.update_context(context = dictionary)

                return render(request, self.template_name, context=dictionary)

            def post(self, request):
                mod_app = ModApp(request.POST)
                dictionary = player_poller.currentPlayers_DB
                dictionary["modform"] = mod_app
                dictionary = viewContext.update_context(context = dictionary)
                if mod_app.is_valid():
                    LOGGER.info("Mod Application submitted!")
                    LOGGER.info(f"Discord ID of applicant: {mod_app.cleaned_data['discord_name']}")
                    mod_app.save()
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
                dictionary = viewContext.update_context(context = dictionary)
                return render(request, self.template_name, context=dictionary)

            def post(self, request):
                admin_app = AdminApp(request.POST)
                dictionary = player_poller.currentPlayers_DB
                dictionary["admin_form"] = admin_app
                dictionary = viewContext.update_context(context = dictionary)
                if admin_app.is_valid():
                    LOGGER.info("Admin Application submitted.!")
                    LOGGER.info(f"Discord ID of applicant: {admin_app.cleaned_data['discord_name']}")
                    admin_app.save()
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
            LOGGER.info("User logged out!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    class Profile_Views():
        """
        Views that are related to User Profiles and their content
        """
        class All_User_Profile(TemplateView):
            """
            Displays all User Profiles
            """
            template_name = join(settings.PROFILES_DIR, 'all_profiles.html')

            def get(self, request):
                instance_dict = player_poller.currentPlayers_DB
                instance_dict = viewContext.update_context(context = instance_dict)

                return render(request, self.template_name, context=instance_dict)
        
        class User_Profile(TemplateView):
            """
            Displays a User's Profile and it's information
            """
            template_name = join(settings.PROFILES_DIR, 'profile.html')

            def get(self, request, profile_name):
                instance_dict = player_poller.currentPlayers_DB
                instance_dict = viewContext.update_context(context = instance_dict)
                try:
                    user_base = User.objects.get(username=profile_name)
                    user_extra = UserProfileInfo.objects.get(user=user_base)
                    try:
                        if settings.DEBUG:
                            instance_dict.update({
                                "displayed_profile": {
                                    "base": {
                                        "username": user_base.username,
                                        "date_joined": user_base.date_joined,
                                        "last_login": user_base.last_login,
                                        "is_staff": user_base.is_staff
                                    },
                                    "extra": {
                                        "picture": f'http://{settings.DOMAIN_NAME}/media/profile_pictures/{user_extra.profile_picture.name.split("/")[1]}',
                                        "mc_username": user_extra.minecraft_username,
                                        "favorite_pack": user_extra.favorite_modpack
                                    }
                                }
                            })
                        else:
                            instance_dict.update({
                                "displayed_profile": {
                                    "base": {
                                        "username": user_base.username,
                                        "date_joined": user_base.date_joined,
                                        "last_login": user_base.last_login,
                                        "is_staff": user_base.is_staff
                                    },
                                    "extra": {
                                        "picture": f'https://{settings.DOMAIN_NAME}/media/profile_pictures/{user_extra.profile_picture.name.split("/")[1]}',
                                        "mc_username": user_extra.minecraft_username,
                                        "favorite_pack": user_extra.favorite_modpack
                                    }
                                }
                            })
                    except IndexError:
                        instance_dict.update({
                        "displayed_profile": {
                            "base": {
                                "username": user_base.username,
                                "date_joined": user_base.date_joined,
                                "last_login": user_base.last_login,
                                "is_staff": user_base.is_staff
                            },
                            "extra": {
                                "mc_username": user_extra.minecraft_username,
                                "favorite_pack": user_extra.favorite_modpack
                            }
                        }
                    }) 
                except User.DoesNotExist:
                    try:
                        discord_user = DiscordUserInfo.objects.get(username=profile_name)
                        instance_dict.update({
                            "displayed_profile": {
                                "base": {
                                    "username": discord_user.username,
                                    "date_joined": discord_user.date_joined,
                                    "last_login": discord_user.last_login,
                                },
                                "extra": {
                                    "picture": discord_user.profile_picture,
                                    "mc_username": discord_user.minecraft_username,
                                    "discord_username": discord_user.tag,
                                    "favorite_pack": discord_user.favorite_modpack
                                }
                            }
                        })
                    except DiscordUserInfo.DoesNotExist:
                        return HttpResponse("A User with the provided username was not found")

                return render(request, self.template_name, context=instance_dict)

        class User_Profile_Edit(LoginRequiredMixin, TemplateView):
            """
            Displays a User's profile details that can be edited, and allows
            changing of said details
            """
            template_name = join(settings.PROFILES_DIR, 'profile_edit.html')
            login_url = '/login/'
            profile_edit_form = DiscordUserInfoForm()
            extra_edit_form = UserProfileInfoForm()

            def get(self, request, profile_name):
                if str(request.user).split('#')[0] == profile_name:
                    instance_dict = player_poller.currentPlayers_DB
                    instance_dict["profile_edit_form"] = self.profile_edit_form
                    instance_dict["extra_edit_form"] = self.extra_edit_form
                    instance_dict = viewContext.update_context(context = instance_dict)
                    try:
                        user_base = User.objects.get(username=profile_name)
                        user_extra = UserProfileInfo.objects.get(user=user_base)
                        try:
                            instance_dict.update({
                                "displayed_profile": {
                                    "base": {
                                        "username": user_base.username,
                                        "date_joined": user_base.date_joined,
                                        "last_login": user_base.last_login,
                                        "is_staff": user_base.is_staff
                                    },
                                    "extra": {
                                        "picture": f'https://shadowraptor.net/media/profile_pictures/{user_extra.profile_picture.name.split("/")[1]}',
                                        "mc_username": user_extra.minecraft_username,
                                        "favorite_pack": user_extra.favorite_modpack
                                    }
                                }
                            })
                        except IndexError:
                            instance_dict.update({
                            "displayed_profile": {
                                "base": {
                                    "username": user_base.username,
                                    "date_joined": user_base.date_joined,
                                    "last_login": user_base.last_login,
                                    "is_staff": user_base.is_staff
                                },
                                "extra": {
                                    "mc_username": user_extra.minecraft_username,
                                    "favorite_pack": user_extra.favorite_modpack
                                }
                            }
                        }) 
                    except User.DoesNotExist:
                        try:
                            discord_user = DiscordUserInfo.objects.get(username=profile_name)
                            instance_dict.update({
                                "displayed_profile": {
                                    "base": {
                                        "username": discord_user.username,
                                        "date_joined": discord_user.date_joined,
                                        "last_login": discord_user.last_login,
                                    },
                                    "extra": {
                                        "picture": f'https://cdn.discordapp.com/avatars/{discord_user.id}/{discord_user.profile_picture}.png',
                                        "mc_username": discord_user.minecraft_username,
                                        "discord_username": discord_user.tag,
                                        "favorite_pack": discord_user.favorite_modpack
                                    }
                                }
                            })
                        except DiscordUserInfo.DoesNotExist:
                            return HttpResponse("A User with the provided username was not found")

                    return render(request, self.template_name, context=instance_dict)

                else: 
                    return redirect('/accessdenied')

            def post(self, request, profile_name):

                profile_edit_form = DiscordUserInfoForm(request.POST)
                extra_edit_form = UserProfileInfoForm(request.POST)
                instance_dict = player_poller.currentPlayers_DB
                instance_dict["profile_edit_form"] = profile_edit_form
                instance_dict["extra_edit_form"] = self.extra_edit_form
                instance_dict = viewContext.update_context(context = instance_dict)
                if profile_edit_form.is_valid() and extra_edit_form.is_valid():
                    LOGGER.info("A User modified their profile details")
                    changed_user = None
                    try:
                        changed_user = DiscordUserInfo.objects.get(tag=request.user)
                    except ObjectDoesNotExist:
                        changed_user_base = User.objects.get(username=request.user)
                        changed_user = UserProfileInfo.objects.get(user=changed_user_base)
                    if profile_edit_form.cleaned_data["minecraft_username"] != '':
                        changed_user.minecraft_username = profile_edit_form.cleaned_data["minecraft_username"]
                    if profile_edit_form.cleaned_data["favorite_modpack"] != '':
                        changed_user.favorite_modpack = profile_edit_form.cleaned_data["favorite_modpack"]
                    if "profile_picture" in request.FILES:
                        changed_user.profile_picture = request.FILES["profile_picture"]
                    changed_user.save()
                    return redirect('../')
                else:
                    instance_dict["profile_edit_form"] = profile_edit_form
                    return render(request, self.template_name, context=instance_dict)

        class Access_Denied(TemplateView):
            """
            Page displayed when a resource cannot be accessed by a user
            """
            template_name = join(settings.RAPTOMC_TEMPLATE_DIR, 'no_access.html')

            def get(self, request):

                dictionary = player_poller.currentPlayers_DB
                dictionary = viewContext.update_context(context = dictionary)
                return render(request, self.template_name, context=dictionary)

    class Ajax_Views():
        """
        Views that return HTML for use in AJAX requests
        """
        class Server_Buttons(TemplateView):
            """
            Returns HTML of server buttons
            Attempts to fetch new info before sending
            """
            def get(self, request):
                if request.headers.get('HX-Request') == "true":
                    template_name = join(settings.RAPTOMC_TEMPLATE_DIR, 'serverButtons.html')
                    return render(request, template_name, context=player_poller.currentPlayers_DB)
                else:
                    return HttpResponseRedirect('../')

        class Server_Modals(TemplateView):
            """
            Returns HTML of server modals, as well as player counts modal
            Attempts to fetch new info before sending
            """
            def get(self, request):
                if request.headers.get('HX-Request') == "true":
                    template_name = join(settings.RAPTOMC_TEMPLATE_DIR, 'serverModals.html')
                    return render(request, template_name, context=player_poller.currentPlayers_DB)
                else:
                    return HttpResponseRedirect('../')

        class Total_Count(TemplateView):
            """
            Returns a simple HttpResponse with the total count of players on all servers
            """
            def get(self, request):
                if request.headers.get('HX-Request') == "true":
                    template_name = join(settings.RAPTOMC_TEMPLATE_DIR, 'playerCounts.html')
                    playerPoll()
                    return render(request, template_name, context=player_poller.currentPlayers_DB)
                else:
                    return HttpResponseRedirect('../')

        class Export_Data(TemplateView):
            """
            Dump JSON data of all servers
            """
            def get(self, request):
                current_servers = export_server_data_full()
                return JsonResponse(current_servers)


