from logging import getLogger
from threading import Thread

from raptorWeb import settings
from raptorbot.discordbot.bot import raptor_bot
from raptorbot.discordbot.util.raptorbot_settings import TOKEN

LOGGER = getLogger('raptorbot.botware')
bot_thread = Thread(target=lambda: raptor_bot.run((TOKEN)))

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
        bot_thread.start()

    def __call__(self, request):
        """
        Code to be executed for each request before
        the view (and later middleware) are called.
        """
        response = self.get_response(request)
        return response
