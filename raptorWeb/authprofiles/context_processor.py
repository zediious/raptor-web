from django.conf import settings

from raptorWeb.authprofiles.models import UserProfileInfo, DiscordUserInfo

BASE_USER_URL = getattr(settings, 'BASE_USER_URL')

def all_users_to_context(request):
    all_default_users = UserProfileInfo.objects.all()
    all_discord_users = DiscordUserInfo.objects.all()
    users_list = []

    for default_user in all_default_users:
        users_list.append(default_user)
    for discord_user in all_discord_users:
        users_list.append(discord_user)
        
    return {"current_members": users_list,
            "base_user_url": BASE_USER_URL}
