from django.contrib.auth import models

from datetime import date

class DiscordAuthManager(models.UserManager):

    def create_new_discord_user(self, user):
        """
        Create new discord user
        """
        discord_tag = f'{user["username"]}#{user["discriminator"]}'
        new_discord_info = self.create(
            id = user["id"],
            tag = discord_tag,
            username = discord_tag.split('#')[0],
            profile_picture = f'https://cdn.discordapp.com/avatars/{user["id"]}/{user["avatar"]}.png',
            pub_flags = user["public_flags"],
            flags = user["flags"],
            locale = user["locale"],
            mfa_enabled = user["mfa_enabled"],
            date_joined = date.today()
        )

        return new_discord_info