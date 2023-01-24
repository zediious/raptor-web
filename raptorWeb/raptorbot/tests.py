from time import sleep

from django.test import TestCase
from raptorbot.models import DiscordGuild, GlobalAnnouncement, ServerAnnouncement
from raptorbot.discordbot.bot import BotProcessManager
from raptorbot.discordbot.util.raptorbot_settings import TOKEN

class ServerTestCase(TestCase):
    def setUp(self):
        pass

    def test_thread_restart(self):
        process_manager = BotProcessManager(TOKEN)
        process_manager.start_process()
        print("Sleeping for 3 seconds")
        sleep(5)
        process_manager.stop_process()
        print("Sleeping for 3 seconds")
        sleep(5)
        process_manager.start_process()
        sleep(5)
        process_manager.stop_process()
