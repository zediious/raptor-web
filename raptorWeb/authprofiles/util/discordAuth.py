from requests import get, post

from raptorWeb import settings

def exchange_code(discord_code):

    data = {
        "client_id": settings.DISCORD_APP_ID,
        "client_secret": settings.DISCORD_APP_SECRET,
        "grant_type": "authorization_code",
        "code": discord_code,
        "redirect_uri": settings.DISCORD_REDIRECT_URL,
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
    discord_tag = f'{new_info["username"]}#{new_info["discriminator"]}'
    discord_user.profile_picture = f'https://cdn.discordapp.com/avatars/{new_info["id"]}/{new_info["avatar"]}.png'
    discord_user.tag = f'{new_info["username"]}#{new_info["discriminator"]}'
    discord_user.username = discord_tag.split('#')[0]
    discord_user.save()
    return discord_user
    