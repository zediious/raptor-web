from logging import getLogger
from time import sleep

from raptorbot.discordbot.bot import BotProcessManager
from raptorbot.discordbot.util.raptorbot_settings import TOKEN

LOGGER = getLogger('raptorbot.botware')
bot_process_manager = BotProcessManager(bot_token=TOKEN)

class RaptorBotWare:
    """
    Handle tasks regarding the RaptorBot app
    """
    def __init__(self, get_response):
        """
        One-time configuration and initialization.
        """
        self.get_response = get_response
        # Run the Discord Bot in new thread
        bot_process_manager.start_process()
        LOGGER.info("A Discord Bot Thread has been created and is now running")

    def __call__(self, request):
        """
        Code to be executed for each request before
        the view (and later middleware) are called.
        """
        response = self.get_response(request)
        return response
