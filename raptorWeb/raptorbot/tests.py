from time import sleep

from django.test import TestCase
from django.conf import settings

from raptorWeb.raptorbot.discordbot.bot import BotProcessManager

DISCORD_BOT_TOKEN = getattr(settings, 'DISCORD_BOT_TOKEN')

class ServerTestCase(TestCase):
    def setUp(self):
        pass

    def test_thread_restart(self):
        process_manager = BotProcessManager(DISCORD_BOT_TOKEN)
        process_manager.start_process()
        print("Sleeping for 3 seconds")
        sleep(5)
        process_manager.stop_process()
        print("Sleeping for 3 seconds")
        sleep(5)
        process_manager.start_process()
        sleep(5)
        process_manager.stop_process()
