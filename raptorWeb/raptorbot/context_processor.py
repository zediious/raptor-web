from django.conf import settings

from raptorWeb.raptormc.models import SiteInformation
from raptorWeb.raptorbot.models import DiscordGuild

def add_discord_guild_data(request):
    site_info: SiteInformation.objects = SiteInformation.objects.get_or_create(pk=1)[0]
    
    try:
        return {"discord_guild": DiscordGuild.objects.get(guild_id=site_info.discord_guild)}

    except DiscordGuild.DoesNotExist:
        return {"no_discord_guild": "none"}