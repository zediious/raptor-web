from django.conf import settings

from raptorWeb.raptorbot.models import DiscordGuild

DISCORD_GUILD = getattr(settings, 'DISCORD_GUILD')

def add_discord_guild_data(request):
    try:
        return {"discord_guild": DiscordGuild.objects.get(guild_id=DISCORD_GUILD)}

    except DiscordGuild.DoesNotExist:
        return {"no_discord_guild": "none"}