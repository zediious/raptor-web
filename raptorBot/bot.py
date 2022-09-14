import os
import discord
from dotenv import load_dotenv
from json import dumps

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

DISCORD_GUILD = 740388741079760937

ANNOUNCEMENT_CHANNEL = 741015006480564254

async def update_announcements(client, message):
    """
    Gets all messages from defined "ANNOUNCEMENT_CHANNEL" and
    places their content in a Dictionary, nested in another
    dictionary keyed by a countered number. Data is saved
    to an "announcements.json" each iteration.
    """
    channel = client.get_channel(ANNOUNCEMENT_CHANNEL)
    if message.channel == channel:

        messages = [message async for message in channel.history(limit=5)]
        announcements = {}

        key = 0
        for message in messages:
            announcements.update({
                "message{}".format(key): {
                    "author": str(message.author),
                    "message": message.content,
                    "date": str(message.created_at.date().strftime('%B %d %Y'))
                    }
            })
            key += 1

        announcementsJSON = open("../raptorWeb/announcements.json", "w")
        announcementsJSON.write(dumps(announcements, indent=4))
        announcementsJSON.close()    

class RaptorClient(discord.Client):

    async def on_ready(self):
        """
        Triggers when the bot has logged in and is ready.
        """
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        """
        Triggers when a message is sent in the Discord Server.
        """
        await update_announcements(client, message)

    async def on_presence_update(self, before, after):
        """
        Triggers when a member's status on the server changes.
        """
        sr_guild = client.get_guild(740388741079760937)
        member_total = len(sr_guild.members)
        online_members = 0

        for member in sr_guild.members:

            if member.status != discord.Status.offline:
                online_members += 1

        discord_info = {
            "totalMembers": member_total,
            "onlineMembers": online_members
        }

        membersJSON = open("../raptorWeb/discordInfo.json", "w")
        membersJSON.write(dumps(discord_info, indent=4))
        membersJSON.close() 

intents = discord.Intents.all()
intents.message_content = True

client = RaptorClient(intents=intents, max_messages=20000)
client.run(TOKEN)
