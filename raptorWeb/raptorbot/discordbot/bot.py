from logging import Logger, getLogger
from threading import Thread
from time import sleep
from typing import Optional
import ctypes

from django.conf import settings
from django.utils.timezone import localtime

import discord
from discord.ext import commands

from raptorWeb.raptormc.models import SiteInformation
from raptorWeb.gameservers.models import Server
from raptorWeb.raptorbot.models import SentEmbedMessage, DiscordBotInternal
from raptorWeb.raptorbot.discordbot.util import announcements, embed, presence, task_check

LOGGER: Logger = getLogger('raptorbot.discordbot.bot')
DISCORD_BOT_DESCRIPTION: str = getattr(settings, 'DISCORD_BOT_DESCRIPTION')

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
        If a Thread is not currently running, create a new Thread object and set
        to class attribute "active_process", then start the Thread running the bot
        """
        if self.is_running == True:
            message: str = ("You cannot start a Thread when one is currently running."
                            f"Currently running Thread: {self.active_process}")
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
            daemon=True,
            name=f'raptorbot_{localtime()}',
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

                task_check.check_tasks.start(raptor_bot)
                LOGGER.info("Started task check loop")

            except Exception as e:
                LOGGER.error(e)


        @raptor_bot.event
        async def on_presence_update(before, after) -> None:
            await presence.update_member_count(raptor_bot)
            await presence.update_invite_link(raptor_bot)
            
            
        @raptor_bot.event
        async def on_message_delete(message) -> None:
            try:
                saved_embed: SentEmbedMessage = await SentEmbedMessage.objects.aget(message_id=message.id)
                bot_stat: DiscordBotInternal = await DiscordBotInternal.objects.aget(name="botinternal-stat")
                bot_stat.deleted_a_message = True
                await bot_stat.asave()
                await DiscordBotInternal.objects.aupdate(
                    deleted_a_message=True
                )
                sleep(3)
                await saved_embed.adelete()
                
            except SentEmbedMessage.DoesNotExist:
                pass
        

        @raptor_bot.event
        async def on_message(message: discord.Message) -> None:
            site_info: SiteInformation = await SiteInformation.objects.aget(pk=1)
            channel: discord.guild.GuildChannel = raptor_bot.get_channel(
                int(site_info.discord_global_announcement_channel))

            if message.channel == channel:
                await announcements.update_global_announcements(raptor_bot)

            server_data: Server.objects = Server.objects.all()

            if (message.author != raptor_bot.user
            and message.author.get_role(int(site_info.discord_staff_role)) != None):
                async for server in server_data:
                    if message.channel != raptor_bot.get_channel(
                    int(server.discord_announcement_channel_id)):
                        continue

                    if server.discord_modpack_role_id in str(message.content):
                        await announcements.update_server_announce(
                            server.modpack_name,
                            bot_instance=raptor_bot,
                            site_info=site_info)
            

        @raptor_bot.event
        async def on_raw_message_edit(message: discord.Message) -> None:
            try:
                if message.data["author"]["id"] != raptor_bot.user.id:
                    site_info: SiteInformation = await SiteInformation.objects.aget(pk=1)
                    if message.channel_id == int(site_info.discord_global_announcement_channel):
                            await announcements.update_global_announcements(raptor_bot)

                    try:
                        server_queryset: Server.objects = Server.objects.filter(
                            discord_announcement_channel_id = message.channel_id)
                            
                        if server_queryset != None:
                            server: Server = await server_queryset.aget()
                            await announcements.update_server_announce(
                                server.modpack_name,
                                bot_instance=raptor_bot,
                                site_info=site_info)

                    except Server.DoesNotExist:
                        pass
                    
            except KeyError:
                pass


        # Commands
        @raptor_bot.tree.command(
            name="display_server_info",
            description="Send a message displaying server information. "
                        "Will update if the server's information is changed.")
        @discord.app_commands.describe(key="Choose a server address prefix. This is the first part "
                                           "of a server's domain/address.")
        async def display_server_info(interaction: discord.Interaction, key: str) -> None:
            """
            Send a message with an embed displaying server information. Take a server's address
            key as a parameter to find displayed server.
            """
            server_data: Server.objects = Server.objects.all()

            async for server in server_data:
                if server.server_address.split(".")[0] == key:
                    message_embeds: list[discord.Embed] = await embed.craft_embed(server)
                    await interaction.response.send_message(embeds=message_embeds)
                    sent_message = await interaction.original_response()
                    
                    await SentEmbedMessage.objects.acreate(
                        server=server,
                        webhook_id='',
                        message_id=sent_message.id,
                        channel_id=sent_message.channel.id
                    )

        @raptor_bot.tree.command(
            name="refresh_announcements",
            description="Update Global Announcements models with new announcements")
        async def refresh_announcements(interaction: discord.Interaction) -> None:
            """
            Update Global Announcements models with new announcements from defined Global Announcement channel
            """
            await announcements.update_global_announcements(raptor_bot)

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
            await interaction.response.send_message(
                embed=discord.Embed(
                    description=("Server Announcements are now being updated with the announcements "
                                "for servers from their respective channels, going back 500 messages."),
                color=0x00ff00),
                ephemeral=True)

            site_info: SiteInformation = await SiteInformation.objects.aget(pk=1)
            await announcements.update_all_server_announce(raptor_bot, site_info)


    def stop_process(self) -> Optional[bool]:
        """
        If a Thread is currently running. raise an Exception to 
        terminate the current class attribute "active_process"
        """
        if self.is_running != True:
            message: str = f"You cannot stop a process when there are none currently running."
            raise Exception(message)

        thread_id: int = self.get_thread_id()

        if thread_id != None:
            if ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(thread_id), 
                ctypes.py_object(SystemExit)) > 1: 
                    ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0) 
                    return None

            self.active_process = None
            self.is_running = False
            return True
