from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from os.path import join
from logging import getLogger
from json import load

from raptorWeb import settings
from raptormc.forms import AdminApp, ModApp, UserForm, UserProfileInfoForm, UserLoginForm, DiscordUserInfoForm
from raptormc.models import InformativeText, User, UserProfileInfo, DiscordUserInfo
from raptormc.jobs import player_poller, playerPoll
from raptormc.util import discordAuth

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
                try:
                    context.update({
                        "home_info": InformativeText.objects.get(name="Homepage Information")
                    })
                except:
                    context.update({
                        "home_info": InformativeText.objects.create(name="Homepage Information", content="Update 'Homepage Information' Model to change this text", pk=1)
                    })
                try:
                    announcementsJSON = open(join(settings.BASE_DIR, 'announcements.json'), "r")
                    discordJSON = open(join(settings.BASE_DIR, 'discordInfo.json'), "r")
                    context.update(load(announcementsJSON))
                    context.update(load(discordJSON))
                except:
                    LOGGER.error("announcements.json and/or discordInfo.json missing. Ensure Discord Bot is running and that your directories are structured correctly.")
                return context

        class Announcements(TemplateView):
            """
            Page containing the last 30 announcements from Discord
            """
            template_name = join(TEMPLATE_DIR_RAPTORMC, 'announcements.html')

            def get_context_data(self, **kwargs):
                context = super().get_context_data(**kwargs)
                context.update(player_poller.currentPlayers_DB)
                try:
                    context.update({
                        "announcement_info": InformativeText.objects.get(name="Announcements Information"),
                    })
                except:
                    context.update({
                        "announcement_info": InformativeText.objects.create(name="Announcements Information", content="Update 'Announcements Information' Model to change this text", pk=11),
                    })
                try:
                    announcement_dict = {
                        "announcements": []
                    }
                    message_json = dict(load(open(join(settings.BASE_DIR, 'announcements.json'), "r")))
                    for message in message_json:
                        announcement_dict["announcements"].append({
                            "author": message_json[message]["author"],
                            "message": message_json[message]["message"],
                            "date": message_json[message]["date"]
                        })
                    context.update(announcement_dict)
                    context.update(load(open(join(settings.BASE_DIR, 'discordInfo.json'), "r")))
                except:
                    LOGGER.error("announcements.json and/or discordInfo.json missing. Ensure Discord Bot is running and that your directories are structured correctly.")
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
                        "rules_info": InformativeText.objects.create(name="Rules Information", content="Update 'Rules Information' Model to change this text", pk=2),
                        "network_rules": InformativeText.objects.create(name="Network Rules", content="Update 'Network Rules' Model to change this text", pk=3)
                    })
                try:
                    discordJSON = open(join(settings.BASE_DIR, 'discordInfo.json'), "r")
                    context.update(load(discordJSON))
                except:
                    LOGGER.error("discordInfo.json missing. Ensure Discord Bot is running and that your directories are structured correctly.")
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
                        "banneditems_info": InformativeText.objects.create(name="Banned Items Information", content="Update 'Banned Items Information' Model to change this text", pk=4),
                    })
                try:
                    discordJSON = open(join(settings.BASE_DIR, 'discordInfo.json'), "r")
                    context.update(load(discordJSON))
                except:
                    LOGGER.error("discordInfo.json missing. Ensure Discord Bot is running and that your directories are structured correctly.")
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
                        "voting_info": InformativeText.objects.create(name="Voting Information", content="Update 'Voting Information' Model to change this text", pk=5),
                    })
                try:
                    discordJSON = open(join(settings.BASE_DIR, 'discordInfo.json'), "r")
                    context.update(load(discordJSON))
                except:
                    LOGGER.error("discordInfo.json missing. Ensure Discord Bot is running and that your directories are structured correctly.")
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
                        "joining_info": InformativeText.objects.create(name="Joining Information", content="Update 'Joining Information' Model to change this text", pk=6),
                        "joining_curse_info": InformativeText.objects.create(name="Using the CurseForge Launcher", content="Update 'Using the CurseForge Launcher' Model to change this text", pk=7),
                        "joining_ftb_info": InformativeText.objects.create(name="Using the FTB Launcher", content="Update 'Using the FTB Launcher' Model to change this text", pk=8),
                        "joining_technic_info": InformativeText.objects.create(name="Using the Technic Launcher", content="Update 'Using the Technic Launcher' Model to change this text", pk=9)
                    })
                try:
                    discordJSON = open(join(settings.BASE_DIR, 'discordInfo.json'), "r")
                    context.update(load(discordJSON))
                except:
                    LOGGER.error("discordInfo.json missing. Ensure Discord Bot is running and that your directories are structured correctly.")
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
                        "staffapp_info": InformativeText.objects.create(name="Staff App Information", content="Update 'Staff App Information' Model to change this text", pk=10),
                    })
                try:
                    discordJSON = open(join(settings.BASE_DIR, 'discordInfo.json'), "r")
                    context.update(load(discordJSON))
                except:
                    LOGGER.error("discordInfo.json missing. Ensure Discord Bot is running and that your directories are structured correctly.")
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
                try:
                    discordJSON = open(join(settings.BASE_DIR, 'discordInfo.json'), "r")
                    dictionary.update(load(discordJSON))
                except:
                    LOGGER.error("discordInfo.json missing. Ensure Discord Bot is running and that your directories are structured correctly.")
                
                return render(request, self.template_name, context=dictionary)

            def post(self,request):

                register_form = UserForm(request.POST)
                extra_form = UserProfileInfoForm(request.POST)

                dictionary = player_poller.currentPlayers_DB
                dictionary["registered"] = self.registered
                dictionary["register_form"] = register_form
                dictionary["extra_form"] = extra_form
                try:
                    discordJSON = open(join(settings.BASE_DIR, 'discordInfo.json'), "r")
                    dictionary.update(load(discordJSON))
                except:
                    LOGGER.error("discordInfo.json missing. Ensure Discord Bot is running and that your directories are structured correctly.")

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

        class UserLogin(TemplateView):
            """
            User Login form
            """
            template_name = join(settings.APPLICATIONS_DIR, 'login.html')
            login_form = UserLoginForm()

            def get(self, request):

                dictionary = player_poller.currentPlayers_DB
                dictionary["login_form"] = self.login_form
                try:
                    discordJSON = open(join(settings.BASE_DIR, 'discordInfo.json'), "r")
                    dictionary.update(load(discordJSON))
                except:
                    LOGGER.error("discordInfo.json missing. Ensure Discord Bot is running and that your directories are structured correctly.")
                
                return render(request, self.template_name, context=dictionary)      

            def post(self, request):

                login_form = UserLoginForm(request.POST)

                dictionary = player_poller.currentPlayers_DB
                dictionary["login_form"] = self.login_form
                try:
                    discordJSON = open(join(settings.BASE_DIR, 'discordInfo.json'), "r")
                    dictionary.update(load(discordJSON))
                except:
                    LOGGER.error("discordInfo.json missing. Ensure Discord Bot is running and that your directories are structured correctly.")

                if login_form.is_valid():

                    username = login_form.cleaned_data["username"]
                    password = login_form.cleaned_data["password"]

                    user = authenticate(username=username, password=password)

                    if user:

                        if user.is_active:

                            LOGGER.info("User logged in!")
                            login(request, user)
                            return HttpResponseRedirect('..')

                        else:

                            return HttpResponse("Account not active")

                    else:

                        LOGGER.info(f"User login attempt failed for user: {username}")
                        dictionary["login_form"] = login_form

                        return render(request, self.template_name, context=dictionary)

        class UserLogin_OAuth(TemplateView):

            def get(self, request):

                return redirect(settings.DISCORD_AUTH_URL)

        class UserLogin_OAuth_Success(TemplateView):

            def get(self, request):

                discord_code = request.GET.get('code')
                user_info = discordAuth.exchange_code(discord_code)
                discord_user = authenticate(request, user=user_info)
                try:
                    login(request, discord_user, backend='raptormc.auth.DiscordAuthBackend')
                except AttributeError:
                    login(request, list(discord_user).pop(), backend='raptormc.auth.DiscordAuthBackend')
                return redirect('../../')

        # @login_required(login_url='/login/')

        class ModApp(TemplateView):
            """
            Moderator Application
            """
            template_name = join(settings.APPLICATIONS_DIR, 'modapp.html')
            mod_app = ModApp()

            def get(self, request):

                dictionary = player_poller.currentPlayers_DB
                dictionary["modform"] = self.mod_app
                try:
                    discordJSON = open(join(settings.BASE_DIR, 'discordInfo.json'), "r")
                    dictionary.update(load(discordJSON))
                except:
                    LOGGER.error("discordInfo.json missing. Ensure Discord Bot is running and that your directories are structured correctly.")

                return render(request, self.template_name, context=dictionary)

            def post(self, request):

                mod_app = ModApp(request.POST)
                dictionary = player_poller.currentPlayers_DB
                dictionary["modform"] = mod_app
                try:
                    discordJSON = open(join(settings.BASE_DIR, 'discordInfo.json'), "r")
                    dictionary.update(load(discordJSON))
                except:
                    LOGGER.error("discordInfo.json missing. Ensure Discord Bot is running and that your directories are structured correctly.")

                if mod_app.is_valid():

                    LOGGER.info("Mod Application submitted!")
                    LOGGER.info(f"Discord ID of applicant: {mod_app.cleaned_data['discord_name']}")
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
                try:
                    discordJSON = open(join(settings.BASE_DIR, 'discordInfo.json'), "r")
                    dictionary.update(load(discordJSON))
                except:
                    LOGGER.error("discordInfo.json missing. Ensure Discord Bot is running and that your directories are structured correctly.")

                return render(request, self.template_name, context=dictionary)

            def post(self, request):

                admin_app = AdminApp(request.POST)
                dictionary = player_poller.currentPlayers_DB
                dictionary["admin_form"] = admin_app
                try:
                    discordJSON = open(join(settings.BASE_DIR, 'discordInfo.json'), "r")
                    dictionary.update(load(discordJSON))
                except:
                    LOGGER.error("discordInfo.json missing. Ensure Discord Bot is running and that your directories are structured correctly.")

                if admin_app.is_valid():

                    LOGGER.info("Admin Application submitted.!")
                    LOGGER.info(f"Discord ID of applicant: {admin_app.cleaned_data['discord_name']}")
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
            LOGGER.info("User logged out!")
            return HttpResponseRedirect('..')

    class Profile_Views():
        """
        Views that are related to User Profiles and their content
        """
        class User_Profile(TemplateView):
            """
            Displays a User's Profile and it's information
            """
            template_name = join(settings.PROFILES_DIR, 'profile.html')

            def get(self, request, profile_name):
                instance_dict = player_poller.currentPlayers_DB
                try:
                    discordJSON = open(join(settings.BASE_DIR, 'discordInfo.json'), "r")
                    instance_dict.update(load(discordJSON))
                except:
                    LOGGER.error("discordInfo.json missing. Ensure Discord Bot is running and that your directories are structured correctly.")
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

            def get(self, request, profile_name):
                if str(request.user).split('#')[0] == profile_name:
                    instance_dict = player_poller.currentPlayers_DB
                    instance_dict["profile_edit_form"] = self.profile_edit_form
                    try:
                        discordJSON = open(join(settings.BASE_DIR, 'discordInfo.json'), "r")
                        instance_dict.update(load(discordJSON))
                    except:
                        LOGGER.error("discordInfo.json missing. Ensure Discord Bot is running and that your directories are structured correctly.")
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
                instance_dict = player_poller.currentPlayers_DB
                instance_dict["profile_edit_form"] = profile_edit_form
                try:
                    discordJSON = open(join(settings.BASE_DIR, 'discordInfo.json'), "r")
                    instance_dict.update(load(discordJSON))
                except:
                    LOGGER.error("discordInfo.json missing. Ensure Discord Bot is running and that your directories are structured correctly.")

                if profile_edit_form.is_valid():

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
                try:
                    discordJSON = open(join(settings.BASE_DIR, 'discordInfo.json'), "r")
                    dictionary.update(load(discordJSON))
                except:
                    LOGGER.error("discordInfo.json missing. Ensure Discord Bot is running and that your directories are structured correctly.")

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
                template_name = join(settings.RAPTOMC_TEMPLATE_DIR, 'serverButtons.html')
                return render(request, template_name, context=player_poller.currentPlayers_DB)

        class Server_Modals(TemplateView):
            """
            Returns HTML of server modals, as well as player counts modal
            Attempts to fetch new info before sending
            """
            def get(self, request):
                template_name = join(settings.RAPTOMC_TEMPLATE_DIR, 'serverModals.html')
                return render(request, template_name, context=player_poller.currentPlayers_DB)

        class Total_Count(TemplateView):
            """
            Returns a simple HttpResponse with the total count of players on all servers
            """
            def get(self, request):
                playerPoll()
                return HttpResponse(player_poller.currentPlayers_DB["totalCount"])
