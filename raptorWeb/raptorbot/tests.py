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
        print("Beginning RaptorBot tests, bot will be started and stopped twice")
        process_manager.start_process()
        print("Sleeping for 5 seconds")
        sleep(5)
        print("Stopping")
        process_manager.stop_process()
        print("Sleeping for 5 seconds")
        sleep(5)
        process_manager.start_process()
        print("Sleeping for 5 seconds")
        sleep(5)
        print("Stopping")
        process_manager.stop_process()
