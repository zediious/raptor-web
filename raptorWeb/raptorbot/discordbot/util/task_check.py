from logging import Logger, getLogger

from discord.ext import tasks

from raptorWeb.raptorbot.models import DiscordBotTasks
from raptorWeb.raptorbot.discordbot.util import announcements, presence

LOGGER: Logger = getLogger('raptorbot.discordbot.util.task_check')

@tasks.loop(seconds=5)
async def check_tasks(bot_instance):
    """
    Check if any task attributes are True, and run the corresponding
    action if so. Set the attribute to False after action is complete.
    """
    tasks: DiscordBotTasks = await DiscordBotTasks.objects.aget_or_create(pk=1)

    if tasks[0].refresh_global_announcements:
        await announcements.update_global_announcements(bot_instance)
        LOGGER.error("ran a task")

    if tasks[0].refresh_server_announcements:
        await announcements.update_all_server_announce(bot_instance)
        LOGGER.error("ran a task")

    if tasks[0].update_members:
        await presence.update_member_count(bot_instance)
        LOGGER.error("ran a task")

    await DiscordBotTasks.objects.aupdate(
        id=1,
        refresh_global_announcements=False,
        refresh_server_announcements=False,
        update_members=False
    )
