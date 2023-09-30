from logging import Logger, getLogger

from django.conf import settings
from django.utils.timezone import localtime

from raptorWeb.raptorbot.discordbot.bot import BotProcessManager
from raptorWeb.raptorbot.models import DiscordBotTasks, DiscordBotInternal

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


def get_bot_status():
    """
    Return the is_active class attribute of bot_process_manager
    """
    return bot_process_manager.is_running

def is_safe_to_start():
    """
    Return true if it has been one minute since the bot last stopped.
    """
    bot_stats = DiscordBotInternal.objects.get_or_create(name="botinternal-stat")[0]
    minutes_since_stop = int(str(
        (localtime() - bot_stats.time_last_stopped.astimezone())
        ).split(":")[1])

    if minutes_since_stop > 1:
        return True

    return False

def start_bot_process():
    """
    Run the Discord Bot in a new thread
    """
    bot_process_manager.start_process()
    LOGGER.info("A Discord Bot Thread has been created and is now running")

def stop_bot_process():
    """
    Terminate the current Discord Bot thread
    """
    if bot_process_manager.stop_process() == True:
        bot_stats = DiscordBotInternal.objects.get_or_create(name="botinternal-stat")[0]
        bot_stats.time_last_stopped = localtime()
        bot_stats.save()
        LOGGER.info("The previous Discord Bot Thread has been stopped.")
    else:
        LOGGER.info("There was an error stopping the Discord Bot")

def send_command_update_global_announcements():
    """
    Update DiscordTasks Model attribute update_global_announcements to True
    """
    tasks: DiscordBotTasks = DiscordBotTasks.objects.get_or_create(pk=1)[0]
    tasks.refresh_global_announcements = True
    tasks.save()
    LOGGER.info(("The command 'refresh_global_announcements' has been sent to the Discord Bot "
                "from the web Control Panel."))

def send_command_update_all_server_announcements():
    """
    Update DiscordTasks Model attribute update_server_announcements to True
    """
    tasks: DiscordBotTasks = DiscordBotTasks.objects.get_or_create(pk=1)[0]
    tasks.refresh_server_announcements = True
    tasks.save()
    LOGGER.info(("The command 'refresh_server_announcements' has been sent to the Discord Bot "
                "from the web Control Panel."))

def send_command_update_members():
    """
    Update DiscordTasks Model attribute update_members to True
    """
    tasks: DiscordBotTasks = DiscordBotTasks.objects.get_or_create(pk=1)[0]
    tasks.update_members = True
    tasks.save()
    LOGGER.info(("The command 'update_members' has been sent to the Discord Bot "
                "from the web Control Panel."))
