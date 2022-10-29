import discord
from os import getenv
from dotenv import load_dotenv
from json import dumps

load_dotenv()
TOKEN = getenv('DISCORD_TOKEN')

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
    try:

        if message.channel == channel:

            messages = [message async for message in channel.history(limit=30)]
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

    except AttributeError:

        if message.channel_id == ANNOUNCEMENT_CHANNEL:

            messages = [message async for message in channel.history(limit=30)]
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

async def update_member_count(client):
    """
    Gets a count of total and online members on a
    provided Discord server, and places them in
    a dictionary. Data is saved to a "discordInfo.json"
    on each iteration.
    """
    server = client.get_guild(DISCORD_GUILD)
    member_total = len(server.members)
    online_members = 0

    for member in server.members:

        if member.status != discord.Status.offline:
            online_members += 1

    discord_info = {
        "totalMembers": member_total,
        "onlineMembers": online_members
    }

    membersJSON = open("../raptorWeb/discordInfo.json", "w")
    membersJSON.write(dumps(discord_info, indent=4))
    membersJSON.close()

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

    async def on_raw_message_edit(client, message):
        """
        Triggers when a message is edited on the server.
        """
        await update_announcements(client, message)

    async def on_presence_update(self, before, after):
        """
        Triggers when a member's status on the server changes.
        """ 
        await update_member_count(client)

intents = discord.Intents.all()
intents.message_content = True

client = RaptorClient(intents=intents, max_messages=20000)
client.run(TOKEN)
