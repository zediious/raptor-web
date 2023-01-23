from django.contrib import admin

from raptorbot.models import DiscordGuild, Announcement, ServerAnnouncement

admin.site.register(DiscordGuild)
admin.site.register(Announcement)
admin.site.register(ServerAnnouncement)
