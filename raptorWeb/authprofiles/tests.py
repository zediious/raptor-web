from django.test import TestCase

from raptorWeb.authprofiles.models import User, UserProfileInfo, DiscordUserInfo
from raptorWeb.authprofiles.util.discordAuth import exchange_code

class UserTestCase(TestCase):
    
    def setUp(self):
        discord_user_data = {
            "id": 215632790786539522,
            "discriminator": 9999,
            "username": "TestingUser",
            "avatar": "6bb2368417c21fa3b9f03a48e19ea3ab",
            "public_flags": 0,
            "flags": 0,
            "locale": 'en-us',
            "mfa_enabled": False
        }

        find_user = DiscordUserInfo.objects.filter(id=discord_user_data["id"])
        if len(find_user) == 0:
            new_user = DiscordUserInfo.objects.create_new_discord_user(discord_user_data)

        user = User.objects.create(
            email = 'test@testman.com',
            username='TestMan102',
            password='badpassword')

        UserProfileInfo.objects.create(
            user = user,
            minecraft_username = 'TestMan2',
            favorite_modpack = 'TestPack2')

    def test_user_values(self):
        default_user = User.objects.get(username = 'TestMan102')
        default_user_extra = UserProfileInfo.objects.get(user=default_user)
        self.assertEqual(default_user.email, 'test@testman.com')
        self.assertEqual(default_user.username, 'TestMan102')
        self.assertEqual(default_user.password, 'badpassword')
        self.assertEqual(default_user_extra.user.username, default_user.username)
        self.assertEqual(default_user_extra.minecraft_username, 'TestMan2')
        self.assertEqual(default_user_extra.favorite_modpack, 'TestPack2')

        discord_user = DiscordUserInfo.objects.get(tag='TestingUser#9999')
        self.assertEqual(discord_user.id, 215632790786539522)
        self.assertEqual(discord_user.tag, 'TestingUser#9999')
        self.assertEqual(discord_user.username, 'TestingUser#9999'.split('#')[0])
        self.assertEqual(discord_user.profile_picture, 'https://cdn.discordapp.com/avatars/215632790786539522/6bb2368417c21fa3b9f03a48e19ea3ab.png')
        self.assertEqual(discord_user.pub_flags, 0)
        self.assertEqual(discord_user.flags, 0)
        self.assertEqual(discord_user.locale, 'en-us')
        self.assertEqual(discord_user.mfa_enabled, False)
