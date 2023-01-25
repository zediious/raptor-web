from django.conf import settings
from django.utils.text import slugify

from raptorWeb.authprofiles.models import UserProfileInfo, DiscordUserInfo

def find_slugged_user(slugged_username):
    """
    Given a slugified username, find the user 
    associated with that username
    """
    all_default_users = UserProfileInfo.objects.all()
    all_discord_users = DiscordUserInfo.objects.all()
    users_list = []

    for default_user in all_default_users:
        users_list.append(default_user)
    for discord_user in all_discord_users:
        users_list.append(discord_user)

    for saved_user in users_list:
        try:
            if str(slugify(saved_user.user.username)) == slugify(slugged_username):
                return saved_user
        except AttributeError:
            if str(slugify(saved_user.username)) == slugify(slugged_username):
                return saved_user