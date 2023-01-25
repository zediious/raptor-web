from django.contrib import admin

from raptorWeb.authprofiles.models import UserProfileInfo, DiscordUserInfo

admin.site.register(UserProfileInfo)
admin.site.register(DiscordUserInfo)
