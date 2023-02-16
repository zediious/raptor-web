from logging import Logger, getLogger

from django.conf import settings

from raptorWeb.raptorbot.discordbot.bot import BotProcessManager

DISCORD_BOT_TOKEN: str = getattr(settings, 'DISCORD_BOT_TOKEN')
LOGGER: Logger = getLogger('raptorbot.botware')
bot_process_manager: BotProcessManager = BotProcessManager(bot_token=DISCORD_BOT_TOKEN)

class RaptorBotWare:
    """
    Handle tasks regarding the RaptorBot app
    """
    def __init__(self, get_response):
        """
        One-time configuration and initialization.
        """
        self.get_response = get_response
        start_bot_process()

    def __call__(self, request):
        """
        Code to be executed for each request before
        the view (and later middleware) are called.
        """
        response = self.get_response(request)
        return response

def start_bot_process():
    """
    Run the Discord Bot in a new thread
    """
    bot_process_manager.start_process()
    LOGGER.info("A Discord Bot Thread has been created and is now running")

def stop_bot_process():
    """
    Terminate the current Discord Bot thread, re-instantiate the bot and thread
    and start the new thread
    """
    bot_process_manager.stop_process()
    LOGGER.info("The previous Discord Bot Thread has been stopped and a new one is now running")
