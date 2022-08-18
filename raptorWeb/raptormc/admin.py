from django.contrib import admin
from raptormc.models import Server, PlayerCount, PlayerName

# Register your models here.

admin.site.register(Server)
admin.site.register(PlayerCount)
admin.site.register(PlayerName)
