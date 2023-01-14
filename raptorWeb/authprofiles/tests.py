from django.test import TestCase
from authprofiles.models import User, UserProfileInfo, DiscordUserInfo


class UserTestCase(TestCase):
    def setUp(self):
        DiscordUserInfo.objects.create(
            id = '0',
            tag='TestMan101#1945',
            username='TestMan',
            profile_picture='https://shadowraptor.net/media/profile_pictures/cyberraptor.jpg',
            pub_flags = '0',
            flags = '0',
            locale='en',
            mfa_enabled='False',
            minecraft_username='TestMan',
            favorite_modpack = 'TestPack')

        user = User.objects.create(
            email = 'test@testman.com',
            username='TestMan102',
            password='badpassword')

        UserProfileInfo.objects.create(
            user = user,
            minecraft_username = 'TestMan2',
            favorite_modpack = 'TestPack2')

    def test_user_get(self):
        default_user = User.objects.get(username = 'TestMan102')
        UserProfileInfo.objects.get(user = default_user)
        DiscordUserInfo.objects.get(username = 'TestMan')