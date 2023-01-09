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