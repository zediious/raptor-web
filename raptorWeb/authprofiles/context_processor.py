from os.path import join
from json import load

from django.conf import settings
from django.http import HttpResponse
from django.utils.timezone import now, localtime

from raptorWeb.authprofiles.models import RaptorUser, UserProfileInfo, DiscordUserInfo

BASE_USER_URL: str = getattr(settings, 'BASE_USER_URL')
BASE_DIR: str = getattr(settings, 'BASE_DIR')
IMPORT_USERS: bool = getattr(settings, 'IMPORT_USERS')

def all_users_to_context(request: HttpResponse) -> dict:
    if IMPORT_USERS == True:
        import_users()
    return {"current_members": RaptorUser.objects.all(),
            "user_path": BASE_USER_URL}

def import_users() -> None:
    """
    Temporary function to import users from old database schema.
    """
    default_users = load(open(join(BASE_DIR, 'normal_user_list.json')))
    discord_users = load(open(join(BASE_DIR, 'discord_user_list.json')))

    for user in default_users:
        default_user_profile_info = default_users[user].get('user_profile_info')
        new_extra = UserProfileInfo.objects.create(
            picture_changed_manually = False
        )
        try:
            new_extra.minecraft_username = default_user_profile_info["minecraft_username"].replace('(', '').replace(')', '').replace('"', '').replace(',', ''),
            new_extra.favorite_modpack = default_user_profile_info["favorite_modpack"]
        except AttributeError as e:
            print(e)
            new_extra.minecraft_username = "",
            new_extra.favorite_modpack = ""
        new_user = RaptorUser.objects.create(
            is_discord_user = False,
            email = default_users[user]["email"],
            username = default_users[user]["username"],
            user_slug = default_users[user]["user_slug"],
            is_active = True,
            date_joined = localtime(now()),
            last_login = localtime(now()),
            user_profile_info = new_extra
        )
        new_extra.save()
        new_user.password = default_users[user]["password"]
        new_user.save()

    for user in discord_users:
        discord_user_profile_info = discord_users[user].get('user_profile_info')
        new_extra = UserProfileInfo.objects.create(
            picture_changed_manually = False
        )
        try:
            new_extra.minecraft_username = discord_user_profile_info["minecraft_username"],
            new_extra.favorite_modpack = discord_user_profile_info["favorite_modpack"]
        except AttributeError as e:
            print(e)
            new_extra.minecraft_username = "",
            new_extra.favorite_modpack = ""
        new_discord = DiscordUserInfo.objects.create(
            id = discord_users[user]["discord_user_info"]["id"],
            tag = discord_users[user]["discord_user_info"]["tag"],
            pub_flags = discord_users[user]["discord_user_info"]["pub_flags"],
            flags = discord_users[user]["discord_user_info"]["flags"],
            locale = discord_users[user]["discord_user_info"]["locale"],
            mfa_enabled = discord_users[user]["discord_user_info"]["mfa_enabled"],
            avatar_string = "defaultavatarstringtobereplaced"
        )

        new_user = RaptorUser.objects.create(
            is_discord_user = True,
            email = "none@gmail.com",
            username = discord_users[user]["username"],
            user_slug = discord_users[user]["user_slug"],
            is_active = True,
            date_joined = localtime(now()),
            last_login = localtime(now()),
            user_profile_info = new_extra,
            discord_user_info = new_discord
        )
        new_extra.save()
        new_discord.save()
        new_user.save()
