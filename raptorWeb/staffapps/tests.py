from django.test import TestCase
from raptorWeb.staffapps.models import ModeratorApplication, AdminApplication

class StaffAppTestCase(TestCase):
    def setUp(self):
        ModeratorApplication.objects.create(
            age = '12',
            time = 'UTC all day',
            mc_name = 'teststaffmod',
            discord_name = 'teststaffmod#1234',
            voice_chat = 'True',
            description = 'I am a good staff member',
            modpacks = 'I know many modpacks',
            experience = 'I have much experience',
            why_join = 'I want to be staff',
            contact_uppers = 'I can contact uppers'
        )

        AdminApplication.objects.create(
            age = '19',
            time = 'UTC all day',
            mc_name = 'teststaffadmin',
            discord_name = 'teststaffadmin#1234',
            voice_chat = 'True',
            description = 'I am a good staff member',
            modpacks = 'I know many modpacks',
            experience = 'I have much experience',
            why_join = 'I want to be staff',
            plugins = 'I know all the plugins',
            api = 'I am familiar with api',
            it_knowledge = 'I am an IT god',
            linux = 'I daily drive Arch',
            ptero = 'I use Pterodactyl'
        )

    def test_user_get(self):
        ModeratorApplication.objects.get(mc_name = 'teststaffmod')
        AdminApplication.objects.get(mc_name = 'teststaffadmin')
