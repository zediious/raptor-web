from logging import Logger, getLogger

from discord.ext import tasks

from raptorWeb.raptormc.models import SiteInformation
from raptorWeb.raptorbot.models import DiscordBotTasks
from raptorWeb.raptorbot.discordbot.util import announcements, presence, embed, messages

LOGGER: Logger = getLogger('raptorbot.discordbot.util.task_check')

@tasks.loop(seconds=5)
async def check_tasks(bot_instance):
    """
    Check if any task attributes are True, and run the corresponding
    action if so. Set the attribute to False after action is complete.
    """
    tasks: DiscordBotTasks = await DiscordBotTasks.objects.aget_or_create(pk=1)
    site_info: SiteInformation = await SiteInformation.objects.aget(pk=1)

    if tasks[0].refresh_global_announcements:
        await announcements.update_global_announcements(bot_instance)

    if tasks[0].refresh_server_announcements:
        await announcements.update_all_server_announce(bot_instance, site_info)

    if tasks[0].update_members:
        await presence.update_member_count(bot_instance)
        
    if tasks[0].update_embeds:
        await embed.update_embeds(bot_instance)
    
    if str(tasks[0].messages_to_delete) != "":
        await messages.delete_messages(bot_instance, str(tasks[0].messages_to_delete))
        
    if str(tasks[0].users_and_roles_to_give) != "":
        await presence.give_role(bot_instance, str(tasks[0].users_and_roles_to_give))

    await DiscordBotTasks.objects.aupdate(
        id=1,
        refresh_global_announcements=False,
        refresh_server_announcements=False,
        update_members=False,
        update_embeds=False,
        messages_to_delete="",
        users_and_roles_to_give=""
    )
