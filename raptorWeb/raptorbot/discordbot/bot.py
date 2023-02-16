from logging import Logger, getLogger
from threading import Thread
import ctypes

from django.conf import settings

import discord
from discord.ext import commands

from raptorWeb.raptorbot.discordbot.util import raptorbot_util

LOGGER: Logger = getLogger('raptorbot.discordbot.bot')
SCRAPE_SERVER_ANNOUNCEMENT: bool = getattr(settings, 'SCRAPE_SERVER_ANNOUNCEMENT')
DISCORD_BOT_DESCRIPTION: str = getattr(settings, 'DISCORD_BOT_DESCRIPTION')
GLOBAL_ANNOUNCEMENT_CHANNEL_ID: int = getattr(settings, 'GLOBAL_ANNOUNCEMENT_CHANNEL_ID')
STAFF_ROLE_ID: int = getattr(settings, 'STAFF_ROLE_ID')

if SCRAPE_SERVER_ANNOUNCEMENT:
    from raptorWeb.gameservers.models import Server

def _bot_start(bot_instance: commands.Bot, bot_token: str) -> None:
    """
    Top-level function to be pickled by "Thread" objects within
    "BotProcessManager" objects. Do not call this directly.
    """
    bot_instance.run(bot_token)

class BotProcessManager:
    """
    Object that manages the starting, destruction, and re-creation of Bot threads.
    """
    def __init__(self, bot_token) -> None:
        self.bot_token = bot_token
        self.active_process = None
        self.is_running = False

    def get_thread_id(self) -> int:
        if self.active_process != None:
            return self.active_process.ident

    def start_process(self) -> None:
        """
        If a Thread is not currently running, start a new Thread running the bot and set
        the running thread to class attribute "active_process"
        """
        if self.is_running == True:
            message: str = ("You cannot start a process when one is currently running."
                            f"Currently running function: {self.active_process}")
            raise Exception(message)

        intents: discord.Intents = discord.Intents.all()
        intents.message_content = True
        intents.members = True
        raptor_bot: commands.Bot = commands.Bot(
            command_prefix='!',
            description=DISCORD_BOT_DESCRIPTION,
            intents=intents)

        self.is_running = True
        self.active_process = Thread(
            target = _bot_start,
            args=(raptor_bot,
            self.bot_token),)
        self.active_process.start()

        """
        The following functions decorated with @raptor_bot are commands and 
        event listeners for the raptor_bot that is currently running. They
        are not called directly within this code.
        """

        # Events
        @raptor_bot.event
        async def on_ready() -> None:
            LOGGER.info(f'Logged in as {raptor_bot.user} (ID: {raptor_bot.user.id})')

            try:
                synced: list[discord.app_commands.AppCommand] = await raptor_bot.tree.sync()
                LOGGER.info(f"Synced {len(synced)} command(s)")

            except Exception as e:
                LOGGER.error(e)


        @raptor_bot.event
        async def on_presence_update() -> None:
            await raptorbot_util.update_member_count(raptor_bot)
        

        @raptor_bot.event
        async def on_message(message: discord.Message) -> None:
            channel: discord.guild.GuildChannel = raptor_bot.get_channel(
                int(GLOBAL_ANNOUNCEMENT_CHANNEL_ID))

            if message.channel == channel:
                await raptorbot_util.update_global_announcements(raptor_bot)

            if SCRAPE_SERVER_ANNOUNCEMENT:
                server_data: Server.objects = Server.objects.all()

                if (message.author != raptor_bot.user
                and message.author.get_role(STAFF_ROLE_ID) != None):
                    async for server in server_data:
                        if message.channel != raptor_bot.get_channel(
                        int(server.discord_announcement_channel_id)):
                            continue

                        if server.discord_modpack_role_id in str(message.content):
                            await raptorbot_util.update_server_announce(
                                server_address=server.server_address,
                                bot_instance=raptor_bot)
            

        @raptor_bot.event
        async def on_raw_message_edit(message: discord.Message) -> None:
            if message.data["author"]["id"] != raptor_bot.user.id:
                if message.channel_id == GLOBAL_ANNOUNCEMENT_CHANNEL_ID:
                        await raptorbot_util.update_global_announcements(raptor_bot)

                if SCRAPE_SERVER_ANNOUNCEMENT:
                    try:
                        server_queryset: Server.objects = Server.objects.filter(
                            discord_announcement_channel_id = message.channel_id)
                            
                        if server_queryset != None:
                            server: Server = await server_queryset.aget()
                            await raptorbot_util.update_server_announce(
                                server_address=server.server_address,
                                bot_instance=raptor_bot)

                    except Server.DoesNotExist:
                        pass

        # Commands
        @raptor_bot.tree.command(
            name="display_server_info",
            description="Send a message with an embed displaying server information.")
        @discord.app_commands.describe(key="Choose a server address prefix")
        async def display_server_info(interaction: discord.Interaction, key: str) -> None:
            """
            Send a message with an embed displaying server information. Take a server's address
            key as a parameter to find displayed server.
            """
            server_data: Server.objects = Server.objects.all()

            async for server in server_data:
                if server.server_address.split(".")[0] == key:
                    message_embeds: list[discord.Embed] = await raptorbot_util.craft_embed(server)
                    await interaction.response.send_message(embeds=message_embeds)


        @raptor_bot.tree.command(
            name="refresh_announcements",
            description="Update Global Announcements models with new announcements")
        async def refresh_announcements(interaction: discord.Interaction) -> None:
            """
            Update Global Announcements models with new announcements from defined Global Announcement channel
            """
            await raptorbot_util.update_global_announcements(raptor_bot)

            await interaction.response.send_message(
                embed=discord.Embed(
                    description="Global Announcements have been refreshed from current Global Announcements channel",
                color=0x00ff00),
                ephemeral=True)


        @raptor_bot.tree.command(
            name="refresh_server_announcements",
            description=("Update Server Announcement models for all servers with new announcements"))
        async def refresh_server_announcements(interaction: discord.Interaction):
            """
            Update Server Announcement models for all servers with new announcements from
            defined announcement channels for each server.
            """
            await raptorbot_util.update_all_server_announce(raptor_bot)
            
            await interaction.response.send_message(
                embed=discord.Embed(
                    description=("Server Announcements have now been updated with the announcements "
                                "for servers from their respective channels, going back 500 messages."),
                color=0x00ff00),
                ephemeral=True)


    def stop_process(self):
        """
        If a Thread is currently running. raise an Exception to 
        terminate the current class attribute "active_process"
        """
        if self.is_running != True:
            message: str = f"You cannot stop a process when there are none currently running."
            raise Exception(message)

        thread_id = self.get_thread_id()

        if thread_id != None:
            res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 
            ctypes.py_object(SystemExit))
            if res > 1: 
                ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0) 
                LOGGER.error('Exception raise failure')
                return None

            self.active_process = None
            self.is_running = False
