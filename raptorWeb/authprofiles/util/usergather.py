from django.conf import settings
from django.utils.text import slugify

from authprofiles.models import UserProfileInfo, DiscordUserInfo

class UserGatherer(object):
    
    all_users = []
    user_url = getattr(settings, 'BASE_USER_URL')


    def update_default_users(self):
        all_default_users = UserProfileInfo.objects.all()
        for default_user in all_default_users:
            if default_user not in self.all_users:
                self.all_users.append(default_user)

    def update_discord_users(self):
        all_discord_users = DiscordUserInfo.objects.all()
        for discord_user in all_discord_users:
            if discord_user not in self.all_users:
                self.all_users.append(discord_user)

    def update_all_users(self):
        self.update_default_users()
        self.update_discord_users()

    def find_slugged_user(self, slugged_username):
        """
        Given a slugified username, find the user 
        associated with that username
        """
        for saved_user in self.all_users:
            try:
                if str(slugify(saved_user.user.username)) == slugify(slugged_username):
                    return saved_user
            except AttributeError:
                if str(slugify(saved_user.username)) == slugify(slugged_username):
                    return saved_user
