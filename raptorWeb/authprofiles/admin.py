from django.contrib import admin
from django.contrib.auth.models import User, Group

from raptorWeb.authprofiles.models import RaptorUser, UserProfileInfo, DiscordUserInfo

admin.site.unregister(User)
admin.site.unregister(Group)

admin.site.register(RaptorUser)
admin.site.register(UserProfileInfo)
admin.site.register(DiscordUserInfo)
