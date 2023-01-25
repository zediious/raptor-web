from raptorWeb.raptorbot.models import DiscordGuild

def add_discord_guild_data(request):
    guilds = DiscordGuild.objects.all()
    for guild in guilds:
        return {"discord_guild": guild}
