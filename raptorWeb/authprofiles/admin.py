from django.contrib import admin

from authprofiles.models import UserProfileInfo, DiscordUserInfo

admin.site.register(UserProfileInfo)
admin.site.register(DiscordUserInfo)
