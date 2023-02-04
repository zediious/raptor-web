from raptorWeb.raptorbot.models import DiscordGuild

def add_discord_guild_data(request):
    if DiscordGuild.objects.count() != 0:
        guilds = DiscordGuild.objects.all()
        for guild in guilds:
            return {"discord_guild": guild}
    else:
        return {"no_discord_guild": "none"}
