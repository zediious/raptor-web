from django.contrib import admin
from django.forms import TextInput, Textarea
from django.db import models

from raptorbot.models import DiscordMemberCount, Announcement, ServerAnnouncement

admin.site.register(DiscordMemberCount)
admin.site.register(Announcement)
admin.site.register(ServerAnnouncement)
