from requests import get, post

from django.utils.text import slugify
from django.conf import settings

from raptorWeb.authprofiles.models import RaptorUser
from raptorWeb.authprofiles.auth import save_image_from_url_to_profile_info

def exchange_code(discord_code):

    data = {
        "client_id": getattr(settings, 'DISCORD_APP_ID'),
        "client_secret": getattr(settings, 'DISCORD_APP_SECRET'),
        "grant_type": "authorization_code",
        "code": discord_code,
        "redirect_uri": getattr(settings, 'DISCORD_REDIRECT_URL'),
        "scope": "identify email guilds"
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = post("https://discord.com/api/oauth2/token", data=data, headers=headers)
    info_response = get("https://discord.com/api/v6/users/@me", headers={
        'Authorization': f'Bearer {response.json()["access_token"]}'
    })
    
    return info_response.json()

def update_user_details(discord_user, new_info):
    base_user = RaptorUser.objects.get(discord_user_info = discord_user)
    discord_tag = f'{new_info["username"]}#{new_info["discriminator"]}'
    if RaptorUser.objects.filter(user_slug=slugify(new_info["username"])).count() > 0:
        username = discord_tag
    else:
        username = discord_tag.split('#')[0]
    if discord_user.avatar_string != new_info["avatar"] and base_user.user_profile_info.picture_changed_manually != True:
        save_image_from_url_to_profile_info(
            model=base_user.user_profile_info,
            url=f'https://cdn.discordapp.com/avatars/{new_info["id"]}/{new_info["avatar"]}.png'
        )
    discord_user.tag = f'{new_info["username"]}#{new_info["discriminator"]}'
    base_user.username = username
    discord_user.save()
    base_user.save()
    return discord_user
    